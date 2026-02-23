from __future__ import annotations

from typing import Any, Generic, TypeVar

from .model import BaseModel
from .storage_json import JSONStorage

Record = dict[str, Any]
T = TypeVar("T", bound=BaseModel)


class Repository(Generic[T]):
    """
    Generic repository for a given BaseModel subclass.

    Notes:
    - Storage is file-backed (JSON list of dict records)
    - Invalid file data is handled by JSONStorage.read() returning []
    - Validations occur via BaseModel.validate() on create/update and load
    """

    def __init__(self, model_cls: type[T], file_path: str) -> None:
        if not issubclass(model_cls, BaseModel):
            raise ValueError("model_cls must be a subclass of BaseModel")

        self.model_cls: type[T] = model_cls
        self.storage: JSONStorage = JSONStorage(file_path)

    def _load_all_raw(self) -> list[Record]:
        return self.storage.read()

    def _dump_all_raw(self, records: list[Record]) -> None:
        self.storage.write(records)

    def _index_by_id(self, records: list[Record]) -> dict[str, Record]:
        index: dict[str, Record] = {}
        for rec in records:
            rec_id = rec.get("id")
            if isinstance(rec_id, str) and rec_id.strip():
                # latest wins if duplicates exist
                index[rec_id] = rec
            else:
                print("[ERROR] Record without valid 'id' found. Skipping.")
        return index

    def all(self) -> list[T]:
        records = self._load_all_raw()
        items: list[T] = []
        for rec in records:
            try:
                items.append(self.model_cls.from_dict(rec))
            except ValueError as exc:
                print(f"[ERROR] Invalid record for {self.model_cls.__name__}: {exc}")
        return items

    def get(self, entity_id: str) -> T | None:
        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id must be a non-empty string")

        records = self._load_all_raw()
        for rec in records:
            if rec.get("id") == entity_id:
                try:
                    return self.model_cls.from_dict(rec)
                except ValueError as exc:
                    print(f"[ERROR] Invalid record for id={entity_id}: {exc}")
                    return None
        return None

    def create(self, obj: T) -> None:
        obj.validate()

        records = self._load_all_raw()
        index = self._index_by_id(records)

        if obj.id in index:
            raise ValueError(
                f"{self.model_cls.__name__} with id '{obj.id}' already exists"
            )

        records.append(obj.to_dict())
        self._dump_all_raw(records)

    def update(self, obj: T) -> None:
        obj.validate()

        records = self._load_all_raw()
        updated = False

        for i, rec in enumerate(records):
            if rec.get("id") == obj.id:
                records[i] = obj.to_dict()
                updated = True
                break

        if not updated:
            raise ValueError(
                f"{self.model_cls.__name__} with id '{obj.id}' does not exist"
            )

        self._dump_all_raw(records)

    def delete(self, entity_id: str) -> None:
        if not isinstance(entity_id, str) or not entity_id.strip():
            raise ValueError("entity_id must be a non-empty string")

        records = self._load_all_raw()
        new_records: list[Record] = [
            rec for rec in records if rec.get("id") != entity_id
        ]

        # Deleting a non-existing id is not an error: keep execution going.
        self._dump_all_raw(new_records)
