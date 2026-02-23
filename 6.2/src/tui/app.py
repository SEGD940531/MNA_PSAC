import curses
import os
import shlex
from typing import Any, Dict, List, Optional

from reservation import ReservationService


def _safe_str(value: Any) -> str:
    return "" if value is None else str(value)


def _to_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# -------------------------
# Loaders
# -------------------------

def _load_reservations(svc: ReservationService) -> List[Dict[str, Any]]:
    items = svc.reservations.all()
    return [r.to_dict() for r in items]


def _load_hotels(svc: ReservationService) -> List[Dict[str, Any]]:
    items = svc.hotels.all()
    return [h.to_dict() for h in items]


def _load_customers(svc: ReservationService) -> List[Dict[str, Any]]:
    items = svc.customers.all()
    return [c.to_dict() for c in items]


def _load_items(svc: ReservationService, view: str) -> List[Dict[str, Any]]:
    if view == "hotels":
        return _load_hotels(svc)
    if view == "customers":
        return _load_customers(svc)
    return _load_reservations(svc)


# -------------------------
# UI
# -------------------------

def _draw(
    stdscr,
    title: str,
    view: str,
    items: List[Dict[str, Any]],
    selected: int,
    status: str,
) -> int:
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    # Header
    stdscr.addstr(0, 0, title[: w - 1])

    # Tabs
    tabs = "[1] Reservations  [2] Hotels  [3] Customers"
    stdscr.addstr(1, 0, tabs[: w - 1])

    # List area
    list_top = 3
    list_bottom = h - 3
    max_rows = max(0, list_bottom - list_top + 1)

    # Clamp selection
    if items:
        selected = max(0, min(selected, len(items) - 1))
    else:
        selected = 0

    # Simple scrolling window
    start = 0
    if selected >= max_rows:
        start = selected - max_rows + 1

    visible = items[start : start + max_rows]

    for i, item in enumerate(visible):
        idx = start + i

        line = ""
        if view == "reservations":
            rid = _safe_str(item.get("id"))
            hid = _safe_str(item.get("hotel_id"))
            cid = _safe_str(item.get("customer_id"))
            rooms = _safe_str(item.get("rooms"))
            status_txt = _safe_str(item.get("status"))
            line = f"{idx+1:>3}. {rid}  hotel={hid} customer={cid} rooms={rooms} status={status_txt}"

        elif view == "hotels":
            hid = _safe_str(item.get("id"))
            name = _safe_str(item.get("name"))
            location = _safe_str(item.get("location"))
            total_rooms = _safe_str(item.get("total_rooms"))
            available_rooms = _safe_str(item.get("available_rooms"))
            line = (
                f"{idx+1:>3}. {hid}  name={name} location={location} "
                f"total={total_rooms} available={available_rooms}"
            )

        else:  # customers
            cid = _safe_str(item.get("id"))
            name = _safe_str(item.get("name"))
            email = _safe_str(item.get("email"))
            line = f"{idx+1:>3}. {cid}  name={name} email={email}"

        line = line[: w - 1]

        if idx == selected:
            stdscr.addstr(list_top + i, 0, line, curses.A_REVERSE)
        else:
            stdscr.addstr(list_top + i, 0, line)

    # Footer help
    if view == "reservations":
        help_line = (
            "UP/DOWN move | Enter view | n new | c cancel | r refresh | 1/2/3 switch | q quit"
        )
    elif view == "hotels":
        help_line = (
            "UP/DOWN move | Enter view | n new | u update | d delete | r refresh | 1/2/3 switch | q quit"
        )
    else:
        help_line = (
            "UP/DOWN move | Enter view | n new | u update | d delete | r refresh | 1/2/3 switch | q quit"
        )

    stdscr.addstr(h - 2, 0, help_line[: w - 1])

    # Status line
    stdscr.addstr(h - 1, 0, status[: w - 1])

    stdscr.refresh()
    return selected


def _prompt(stdscr, prompt: str) -> str:
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h - 1, 0, " " * (w - 1))
    stdscr.addstr(h - 1, 0, prompt[: w - 1])
    stdscr.refresh()

    curses.echo()
    try:
        value = stdscr.getstr(h - 1, min(len(prompt), w - 2)).decode("utf-8")
    finally:
        curses.noecho()

    return value.strip()


def _view_details(stdscr, title: str, lines: List[str]) -> None:
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    payload = [title, ""] + lines + ["", "Press any key to return"]
    for i, line in enumerate(payload[: h - 1]):
        stdscr.addstr(i, 0, line[: w - 1])

    stdscr.refresh()
    stdscr.getch()


def _details_lines(view: str, item: Dict[str, Any]) -> List[str]:
    if view == "reservations":
        return [
            f"id: {_safe_str(item.get('id'))}",
            f"hotel_id: {_safe_str(item.get('hotel_id'))}",
            f"customer_id: {_safe_str(item.get('customer_id'))}",
            f"rooms: {_safe_str(item.get('rooms'))}",
            f"status: {_safe_str(item.get('status'))}",
            f"created_at: {_safe_str(item.get('created_at'))}",
            f"canceled_at: {_safe_str(item.get('canceled_at'))}",
        ]

    if view == "hotels":
        return [
            f"id: {_safe_str(item.get('id'))}",
            f"name: {_safe_str(item.get('name'))}",
            f"location: {_safe_str(item.get('location'))}",
            f"total_rooms: {_safe_str(item.get('total_rooms'))}",
            f"available_rooms: {_safe_str(item.get('available_rooms'))}",
        ]

    return [
        f"id: {_safe_str(item.get('id'))}",
        f"name: {_safe_str(item.get('name'))}",
        f"email: {_safe_str(item.get('email'))}",
    ]


# -------------------------
# Actions
# -------------------------

def _create_reservation(stdscr, svc: ReservationService) -> str:
    customer_id = _prompt(stdscr, "customer-id: ")
    hotel_id = _prompt(stdscr, "hotel-id: ")
    rooms_str = _prompt(stdscr, "rooms: ")
    rooms = _to_int(rooms_str, default=-1)
    if rooms <= 0:
        return "Invalid rooms (must be positive int)"

    res = svc.create_reservation(customer_id=customer_id, hotel_id=hotel_id, rooms=rooms)
    if res is None:
        return "Create reservation FAILED"
    return f"Created reservation {res.id}"


def _cancel_reservation(svc: ReservationService, rid: str) -> str:
    ok = svc.cancel_reservation(rid)
    return f"Canceled {rid}" if ok else f"Cancel FAILED for {rid}"


def _create_hotel(stdscr, svc: ReservationService) -> str:
    hid = _prompt(stdscr, "id: ")
    name = _prompt(stdscr, "name: ")
    location = _prompt(stdscr, "location: ")
    total_rooms = _to_int(_prompt(stdscr, "total-rooms: "), default=-1)
    available_rooms = _to_int(_prompt(stdscr, "available-rooms: "), default=-1)

    if total_rooms < 0 or available_rooms < 0:
        return "Invalid rooms values (must be non-negative int)"

    ok = svc.create_hotel(
        __import__("reservation").Hotel(
            id=hid,
            name=name,
            location=location,
            total_rooms=total_rooms,
            available_rooms=available_rooms,
        )
    )
    return "Created hotel" if ok else "Create hotel FAILED"


def _update_hotel(stdscr, svc: ReservationService, hid: str) -> str:
    current = svc.get_hotel(hid)
    if current is None:
        return f"Hotel '{hid}' not found"

    # Allow blank to keep current
    name = _prompt(stdscr, f"name [{current.name}]: ")
    location = _prompt(stdscr, f"location [{current.location}]: ")
    total_rooms_str = _prompt(stdscr, f"total-rooms [{current.total_rooms}]: ")
    available_rooms_str = _prompt(stdscr, f"available-rooms [{current.available_rooms}]: ")

    changes: Dict[str, Any] = {}
    if name.strip():
        changes["name"] = name.strip()
    if location.strip():
        changes["location"] = location.strip()
    if total_rooms_str.strip():
        changes["total_rooms"] = _to_int(total_rooms_str.strip(), default=current.total_rooms)
    if available_rooms_str.strip():
        changes["available_rooms"] = _to_int(available_rooms_str.strip(), default=current.available_rooms)

    ok = svc.update_hotel(hid, **changes)
    return "Updated hotel" if ok else "Update hotel FAILED"


def _delete_hotel(stdscr, svc: ReservationService, hid: str) -> str:
    confirm = _prompt(stdscr, f"Delete hotel {hid}? type YES: ")
    if confirm != "YES":
        return "Delete canceled"

    ok = svc.delete_hotel(hid)
    return "Deleted hotel" if ok else "Delete hotel FAILED"


def _create_customer(stdscr, svc: ReservationService) -> str:
    cid = _prompt(stdscr, "id: ")
    name = _prompt(stdscr, "name: ")
    email = _prompt(stdscr, "email: ")

    ok = svc.create_customer(
        __import__("reservation").Customer(
            id=cid,
            name=name,
            email=email,
        )
    )
    return "Created customer" if ok else "Create customer FAILED"


def _update_customer(stdscr, svc: ReservationService, cid: str) -> str:
    current = svc.get_customer(cid)
    if current is None:
        return f"Customer '{cid}' not found"

    name = _prompt(stdscr, f"name [{current.name}]: ")
    email = _prompt(stdscr, f"email [{current.email}]: ")

    changes: Dict[str, Any] = {}
    if name.strip():
        changes["name"] = name.strip()
    if email.strip():
        changes["email"] = email.strip()

    ok = svc.update_customer(cid, **changes)
    return "Updated customer" if ok else "Update customer FAILED"


def _delete_customer(stdscr, svc: ReservationService, cid: str) -> str:
    confirm = _prompt(stdscr, f"Delete customer {cid}? type YES: ")
    if confirm != "YES":
        return "Delete canceled"

    ok = svc.delete_customer(cid)
    return "Deleted customer" if ok else "Delete customer FAILED"


# -------------------------
# Entrypoint
# -------------------------

def run_tui(base_dir: str) -> int:
    svc = ReservationService(base_dir=base_dir)

    def _main(stdscr) -> int:
        curses.curs_set(0)
        stdscr.keypad(True)

        view = "reservations"  # reservations | hotels | customers
        status = "Ready"
        selected = 0
        items = _load_items(svc, view)

        while True:
            title = f"TUI (storage={base_dir}) view={view}"
            selected = _draw(stdscr, title, view, items, selected, status)
            ch = stdscr.getch()

            if ch in (ord("q"), ord("Q")):
                return 0

            # Switch tabs
            if ch == ord("1"):
                view = "reservations"
                items = _load_items(svc, view)
                selected = 0
                status = f"Switched to {view}"
                continue

            if ch == ord("2"):
                view = "hotels"
                items = _load_items(svc, view)
                selected = 0
                status = f"Switched to {view}"
                continue

            if ch == ord("3"):
                view = "customers"
                items = _load_items(svc, view)
                selected = 0
                status = f"Switched to {view}"
                continue

            if ch == curses.KEY_UP:
                selected = max(0, selected - 1)
                status = "Ready"
                continue

            if ch == curses.KEY_DOWN:
                selected = min(max(0, len(items) - 1), selected + 1)
                status = "Ready"
                continue

            if ch in (ord("r"), ord("R")):
                items = _load_items(svc, view)
                selected = min(selected, max(0, len(items) - 1))
                status = f"Refreshed ({len(items)} items)"
                continue

            if ch in (curses.KEY_ENTER, 10, 13):
                if not items:
                    status = "No items"
                    continue
                _view_details(stdscr, f"Details ({view})", _details_lines(view, items[selected]))
                status = "Ready"
                continue

            # Create
            if ch in (ord("n"), ord("N")):
                if view == "reservations":
                    status = _create_reservation(stdscr, svc)
                elif view == "hotels":
                    status = _create_hotel(stdscr, svc)
                else:
                    status = _create_customer(stdscr, svc)

                items = _load_items(svc, view)
                selected = min(selected, max(0, len(items) - 1))
                continue

            # Reservations: cancel
            if view == "reservations" and ch in (ord("c"), ord("C")):
                if not items:
                    status = "No reservations"
                    continue
                rid = _safe_str(items[selected].get("id"))
                status = _cancel_reservation(svc, rid)
                items = _load_items(svc, view)
                selected = min(selected, max(0, len(items) - 1))
                continue

            # Hotels/Customers: update
            if view in {"hotels", "customers"} and ch in (ord("u"), ord("U")):
                if not items:
                    status = "No items"
                    continue

                item_id = _safe_str(items[selected].get("id"))
                if view == "hotels":
                    status = _update_hotel(stdscr, svc, item_id)
                else:
                    status = _update_customer(stdscr, svc, item_id)

                items = _load_items(svc, view)
                selected = min(selected, max(0, len(items) - 1))
                continue

            # Hotels/Customers: delete
            if view in {"hotels", "customers"} and ch in (ord("d"), ord("D")):
                if not items:
                    status = "No items"
                    continue

                item_id = _safe_str(items[selected].get("id"))
                if view == "hotels":
                    status = _delete_hotel(stdscr, svc, item_id)
                else:
                    status = _delete_customer(stdscr, svc, item_id)

                items = _load_items(svc, view)
                selected = min(selected, max(0, len(items) - 1))
                continue

            status = "Unknown key"

    return curses.wrapper(_main)