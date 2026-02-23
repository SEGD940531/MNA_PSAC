from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from persistence.model import BaseModel


def _now_iso() -> str:
    # ISO timestamp for traceability in JSON
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Hotel(BaseModel):
    """
    Hotel entity.

    Notes:
    - total_rooms represents capacity
    - available_rooms is mutable via reserve/cancel flows
    """

    entity_name = "hotel"

    name: str = ""
    location: str = ""
    total_rooms: int = 0
    available_rooms: int = 0

    def validate(self) -> None:
        super().validate()

        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("hotel.name must be a non-empty string")
        if not isinstance(self.location, str) or not self.location.strip():
            raise ValueError("hotel.location must be a non-empty string")

        if not isinstance(self.total_rooms, int) or self.total_rooms < 0:
            raise ValueError("hotel.total_rooms must be a non-negative int")

        if not isinstance(self.available_rooms, int) or self.available_rooms < 0:
            raise ValueError("hotel.available_rooms must be a non-negative int")

        if self.available_rooms > self.total_rooms:
            raise ValueError("hotel.available_rooms cannot exceed hotel.total_rooms")


@dataclass
class Customer(BaseModel):
    """Customer entity."""

    entity_name = "customer"

    name: str = ""
    email: str = ""

    def validate(self) -> None:
        super().validate()

        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("customer.name must be a non-empty string")
        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("customer.email must be a non-empty string")


@dataclass
class Reservation(BaseModel):
    """
    Reservation entity.

    status:
    - active
    - canceled
    """

    entity_name = "reservation"

    hotel_id: str = ""
    customer_id: str = ""
    rooms: int = 1
    status: str = "active"
    created_at: str = field(default_factory=_now_iso)
    canceled_at: str = ""

    def validate(self) -> None:
        super().validate()

        if not isinstance(self.hotel_id, str) or not self.hotel_id.strip():
            raise ValueError("reservation.hotel_id must be a non-empty string")
        if not isinstance(self.customer_id, str) or not self.customer_id.strip():
            raise ValueError("reservation.customer_id must be a non-empty string")

        if not isinstance(self.rooms, int) or self.rooms <= 0:
            raise ValueError("reservation.rooms must be a positive int")

        if self.status not in {"active", "canceled"}:
            raise ValueError("reservation.status must be 'active' or 'canceled'")

        if not isinstance(self.created_at, str) or not self.created_at.strip():
            raise ValueError("reservation.created_at must be a non-empty string")

        if self.status == "canceled" and (
            not isinstance(self.canceled_at, str) or not self.canceled_at.strip()
        ):
            raise ValueError(
                "reservation.canceled_at is required when status is canceled"
            )
