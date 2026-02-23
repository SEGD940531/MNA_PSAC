import os
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from persistence.repository import Repository

from .models import Customer, Hotel, Reservation


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReservationService:
    """
    Application service that orchestrates persistence behaviors.

    This service prints errors and continues execution (returns None/False)
    to satisfy the "execution must continue" requirement.
    """

    def __init__(self, base_dir: str = "store") -> None:
        if not isinstance(base_dir, str) or not base_dir.strip():
            raise ValueError("base_dir must be a non-empty string")

        os.makedirs(base_dir, exist_ok=True)

        hotels_path = os.path.join(base_dir, "hotels.json")
        customers_path = os.path.join(base_dir, "customers.json")
        reservations_path = os.path.join(base_dir, "reservations.json")

        self.hotels = Repository(Hotel, hotels_path)
        self.customers = Repository(Customer, customers_path)
        self.reservations = Repository(Reservation, reservations_path)

    # -------------------------
    # Hotel operations
    # -------------------------
    def create_hotel(self, hotel: Hotel) -> bool:
        try:
            # If available_rooms not set, default to total_rooms
            if hotel.available_rooms == 0 and hotel.total_rooms > 0:
                hotel = replace(hotel, available_rooms=hotel.total_rooms)

            self.hotels.create(hotel)
            return True
        except ValueError as exc:
            print(f"[ERROR] create_hotel failed: {exc}")
            return False

    def delete_hotel(self, hotel_id: str) -> bool:
        try:
            self.hotels.delete(hotel_id)
            return True
        except ValueError as exc:
            print(f"[ERROR] delete_hotel failed: {exc}")
            return False

    def get_hotel(self, hotel_id: str) -> Hotel | None:
        try:
            return self.hotels.get(hotel_id)
        except ValueError as exc:
            print(f"[ERROR] get_hotel failed: {exc}")
            return None

    def update_hotel(self, hotel_id: str, **changes: Any) -> bool:
        try:
            current = self.hotels.get(hotel_id)
            if current is None:
                print(f"[ERROR] update_hotel failed: hotel '{hotel_id}' not found")
                return False

            new_total = changes.get("total_rooms", current.total_rooms)
            new_available = changes.get("available_rooms", current.available_rooms)

            updated = replace(
                current,
                name=changes.get("name", current.name),
                location=changes.get("location", current.location),
                total_rooms=new_total,
                available_rooms=new_available,
            )
            updated.validate()
            self.hotels.update(updated)
            return True
        except ValueError as exc:
            print(f"[ERROR] update_hotel failed: {exc}")
            return False

    def display_hotel(self, hotel_id: str) -> dict[str, Any] | None:
        hotel = self.get_hotel(hotel_id)
        return hotel.to_dict() if hotel else None

    # -------------------------
    # Customer operations
    # -------------------------
    def create_customer(self, customer: Customer) -> bool:
        try:
            self.customers.create(customer)
            return True
        except ValueError as exc:
            print(f"[ERROR] create_customer failed: {exc}")
            return False

    def delete_customer(self, customer_id: str) -> bool:
        try:
            self.customers.delete(customer_id)
            return True
        except ValueError as exc:
            print(f"[ERROR] delete_customer failed: {exc}")
            return False

    def get_customer(self, customer_id: str) -> Customer | None:
        try:
            return self.customers.get(customer_id)
        except ValueError as exc:
            print(f"[ERROR] get_customer failed: {exc}")
            return None

    def update_customer(self, customer_id: str, **changes: Any) -> bool:
        try:
            current = self.customers.get(customer_id)
            if current is None:
                print(
                    f"[ERROR] update_customer failed: customer '{customer_id}' not found"
                )
                return False

            updated = replace(
                current,
                name=changes.get("name", current.name),
                email=changes.get("email", current.email),
            )
            updated.validate()
            self.customers.update(updated)
            return True
        except ValueError as exc:
            print(f"[ERROR] update_customer failed: {exc}")
            return False

    def display_customer(self, customer_id: str) -> dict[str, Any] | None:
        customer = self.get_customer(customer_id)
        return customer.to_dict() if customer else None

    # -------------------------
    # Reservation operations
    # -------------------------
    def create_reservation(
        self, customer_id: str, hotel_id: str, rooms: int = 1
    ) -> Reservation | None:
        try:
            customer = self.customers.get(customer_id)
            if customer is None:
                print(
                    f"[ERROR] create_reservation failed: customer '{customer_id}' not found"
                )
                return None

            hotel = self.hotels.get(hotel_id)
            if hotel is None:
                print(
                    f"[ERROR] create_reservation failed: hotel '{hotel_id}' not found"
                )
                return None

            if not isinstance(rooms, int) or rooms <= 0:
                print("[ERROR] create_reservation failed: rooms must be a positive int")
                return None

            if hotel.available_rooms < rooms:
                print("[ERROR] create_reservation failed: not enough available rooms")
                return None

            # Decrease availability
            updated_hotel = replace(
                hotel, available_rooms=hotel.available_rooms - rooms
            )
            updated_hotel.validate()
            self.hotels.update(updated_hotel)

            res = Reservation(
                id=str(uuid4()),
                hotel_id=hotel_id,
                customer_id=customer_id,
                rooms=rooms,
                status="active",
                created_at=_now_iso(),
            )
            res.validate()
            self.reservations.create(res)
            return res

        except ValueError as exc:
            print(f"[ERROR] create_reservation failed: {exc}")
            return None

    def cancel_reservation(self, reservation_id: str) -> bool:
        try:
            res = self.reservations.get(reservation_id)
            if res is None:
                # Not an error per requirement: continue execution
                print(
                    f"[ERROR] cancel_reservation: reservation '{reservation_id}' not found"
                )
                return False

            if res.status == "canceled":
                return True

            hotel = self.hotels.get(res.hotel_id)
            if hotel is None:
                print(f"[ERROR] cancel_reservation: hotel '{res.hotel_id}' not found")
                return False

            # Restore availability
            restored = replace(hotel, available_rooms=hotel.available_rooms + res.rooms)
            restored.validate()
            self.hotels.update(restored)

            canceled = replace(res, status="canceled", canceled_at=_now_iso())
            canceled.validate()
            self.reservations.update(canceled)
            return True

        except ValueError as exc:
            print(f"[ERROR] cancel_reservation failed: {exc}")
            return False

    def get_reservation(self, reservation_id: str) -> Reservation | None:
        try:
            return self.reservations.get(reservation_id)
        except ValueError as exc:
            print(f"[ERROR] get_reservation failed: {exc}")
            return None

    def display_reservation(self, reservation_id: str) -> dict[str, Any] | None:
        res = self.get_reservation(reservation_id)
        return res.to_dict() if res else None
