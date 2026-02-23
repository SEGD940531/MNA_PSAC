from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Any, ClassVar, Self, TypedDict


class BaseModelDict(TypedDict):
    id: str


@dataclass
class BaseModel:
    """
    Base class for domain entities.

    Subclasses should:
    - declare entity_name (like a table name)
    - define their fields as dataclass attributes
    - override validate() for domain rules
    """

    id: str
    entity_name: ClassVar[str] = ""

    def validate(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("id must be a non-empty string")

    def to_dict(self) -> dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError("BaseModel subclasses must be dataclasses")
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")

        if not is_dataclass(cls):
            raise TypeError("BaseModel subclasses must be dataclasses")

        allowed: set[str] = {f.name for f in fields(cls)}
        filtered: dict[str, Any] = {k: v for k, v in data.items() if k in allowed}

        obj = cls(**filtered)
        obj.validate()
        return obj
