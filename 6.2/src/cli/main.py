import os
import shlex
import sys
from typing import List, Optional

from reservation import ReservationService


def _print_help() -> None:
    print(
        "\nCommands:\n"
        "  hotels create --id <id> --name <name> --location <loc> --total-rooms <n> --available-rooms <n>\n"
        "  hotels display --id <id>\n"
        "  hotels list\n"
        "  hotels delete --id <id>\n"
        "  hotels update --id <id> [--name ...] [--location ...] [--total-rooms ...] [--available-rooms ...]\n"
        "\n"
        "  customers create --id <id> --name <name> --email <email>\n"
        "  customers display --id <id>\n"
        "  customers list\n"
        "  customers delete --id <id>\n"
        "  customers update --id <id> [--name ...] [--email ...]\n"
        "\n"
        "  reservations create --customer-id <cid> --hotel-id <hid> --rooms <n>\n"
        "  reservations display --id <id>\n"
        "  reservations list\n"
        "  reservations cancel --id <id>\n"
        "\n"
        "Interactive:\n"
        "  help\n"
        "  exit | quit\n"
    )


def _get_flag_value(args: List[str], flag: str) -> Optional[str]:
    if flag not in args:
        return None
    idx = args.index(flag)
    if idx + 1 >= len(args):
        return None
    return args[idx + 1]


def _has_flag(args: List[str], flag: str) -> bool:
    return flag in args


def _to_int(value: Optional[str], default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _execute(argv: List[str], svc: ReservationService) -> int:
    if not argv:
        return 0

    cmd = argv[0].strip().lower()

    if cmd in {"help", "-h", "--help"}:
        _print_help()
        return 0

    if cmd == "shell":
        return _interactive_shell(svc)

    if len(argv) < 2:
        print("[ERROR] Missing subcommand. Try: help")
        return 1

    group = argv[0].lower()
    action = argv[1].lower()
    rest = argv[2:]

    # -------------------------
    # Hotels
    # -------------------------
    if group == "hotels":
        if action == "create":
            hid = _get_flag_value(rest, "--id") or ""
            name = _get_flag_value(rest, "--name") or ""
            location = _get_flag_value(rest, "--location") or ""
            total_rooms = _to_int(_get_flag_value(rest, "--total-rooms"), 0)
            available_rooms = _to_int(_get_flag_value(rest, "--available-rooms"), 0)

            ok = svc.create_hotel(
                # Note: Hotel is imported from reservation package
                __import__("reservation").Hotel(
                    id=hid,
                    name=name,
                    location=location,
                    total_rooms=total_rooms,
                    available_rooms=available_rooms,
                )
            )
            print("OK" if ok else "FAILED")
            return 0

        if action == "display":
            hid = _get_flag_value(rest, "--id") or ""
            data = svc.display_hotel(hid)
            print(data if data is not None else "NOT_FOUND")
            return 0

        if action == "list":
            items = svc.hotels.all()
            print([h.to_dict() for h in items])
            return 0

        if action == "delete":
            hid = _get_flag_value(rest, "--id") or ""
            ok = svc.delete_hotel(hid)
            print("OK" if ok else "FAILED")
            return 0

        if action == "update":
            hid = _get_flag_value(rest, "--id") or ""
            changes = {}
            if _has_flag(rest, "--name"):
                changes["name"] = _get_flag_value(rest, "--name") or ""
            if _has_flag(rest, "--location"):
                changes["location"] = _get_flag_value(rest, "--location") or ""
            if _has_flag(rest, "--total-rooms"):
                changes["total_rooms"] = _to_int(_get_flag_value(rest, "--total-rooms"), 0)
            if _has_flag(rest, "--available-rooms"):
                changes["available_rooms"] = _to_int(_get_flag_value(rest, "--available-rooms"), 0)

            ok = svc.update_hotel(hid, **changes)
            print("OK" if ok else "FAILED")
            return 0

        print("[ERROR] Unknown hotels action")
        return 1

    # -------------------------
    # Customers
    # -------------------------
    if group == "customers":
        if action == "create":
            cid = _get_flag_value(rest, "--id") or ""
            name = _get_flag_value(rest, "--name") or ""
            email = _get_flag_value(rest, "--email") or ""

            ok = svc.create_customer(
                __import__("reservation").Customer(
                    id=cid,
                    name=name,
                    email=email,
                )
            )
            print("OK" if ok else "FAILED")
            return 0

        if action == "display":
            cid = _get_flag_value(rest, "--id") or ""
            data = svc.display_customer(cid)
            print(data if data is not None else "NOT_FOUND")
            return 0

        if action == "list":
            items = svc.customers.all()
            print([c.to_dict() for c in items])
            return 0

        if action == "delete":
            cid = _get_flag_value(rest, "--id") or ""
            ok = svc.delete_customer(cid)
            print("OK" if ok else "FAILED")
            return 0

        if action == "update":
            cid = _get_flag_value(rest, "--id") or ""
            changes = {}
            if _has_flag(rest, "--name"):
                changes["name"] = _get_flag_value(rest, "--name") or ""
            if _has_flag(rest, "--email"):
                changes["email"] = _get_flag_value(rest, "--email") or ""

            ok = svc.update_customer(cid, **changes)
            print("OK" if ok else "FAILED")
            return 0

        print("[ERROR] Unknown customers action")
        return 1

    # -------------------------
    # Reservations
    # -------------------------
    if group == "reservations":
        if action == "create":
            cid = _get_flag_value(rest, "--customer-id") or ""
            hid = _get_flag_value(rest, "--hotel-id") or ""
            rooms = _to_int(_get_flag_value(rest, "--rooms"), 1)

            res = svc.create_reservation(customer_id=cid, hotel_id=hid, rooms=rooms)
            print(res.to_dict() if res is not None else "FAILED")
            return 0

        if action == "display":
            rid = _get_flag_value(rest, "--id") or ""
            data = svc.display_reservation(rid)
            print(data if data is not None else "NOT_FOUND")
            return 0

        if action == "list":
            items = svc.reservations.all()
            print([r.to_dict() for r in items])
            return 0

        if action == "cancel":
            rid = _get_flag_value(rest, "--id") or ""
            ok = svc.cancel_reservation(rid)
            print("OK" if ok else "FAILED")
            return 0

        print("[ERROR] Unknown reservations action")
        return 1

    print("[ERROR] Unknown command group. Try: help")
    return 1


def _interactive_shell(svc: ReservationService) -> int:
    print("Reservation shell. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        try:
            line = input("store> ").strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 0

        if not line:
            continue

        if line.lower() in {"exit", "quit"}:
            return 0

        if line.lower() == "help":
            _print_help()
            continue

        argv = shlex.split(line)
        _execute(argv, svc)

    return 0


def main() -> None:
    base_dir = os.getenv("STORAGE_DIR", "store")
    svc = ReservationService(base_dir=base_dir)

    # If called from Makefile with ARGS="..."
    if len(sys.argv) > 1:
        sys.exit(_execute(sys.argv[1:], svc))

    # If no args, open interactive shell by default
    sys.exit(_interactive_shell(svc))


if __name__ == "__main__":
    main()