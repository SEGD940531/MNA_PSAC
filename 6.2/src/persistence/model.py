from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, ClassVar, Dict, Type, TypeVar


T = TypeVar("T", bound="BaseModel")


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
        """Override in subclasses for entity-specific validation."""
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("id must be a non-empty string")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the dataclass to a plain dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create an instance from a dict.

        This method ignores unknown keys and relies on dataclass defaults
        for missing optional fields.
        """
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")

        allowed = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in allowed}

        obj = cls(**filtered)  # type: ignore[arg-type]
        obj.validate()
        return obj