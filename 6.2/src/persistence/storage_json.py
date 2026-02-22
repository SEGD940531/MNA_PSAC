from __future__ import annotations

import json
import os
from typing import Any, List


class JSONStorage:
    """
    Simple JSON file storage.

    Stores a list of dict records in a JSON file.
    - If the file does not exist, read() returns []
    - If the file contains invalid JSON, read() prints an error and returns []
    """

    def __init__(self, file_path: str) -> None:
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path must be a non-empty string")
        self.file_path = file_path

    def read(self) -> List[dict]:
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw: Any = json.load(f)

            if raw is None:
                return []
            if not isinstance(raw, list):
                print(
                    f"[ERROR] Invalid data format in file: {self.file_path}. "
                    "Expected a JSON list."
                )
                return []

            normalized: List[dict] = []
            for idx, item in enumerate(raw):
                if isinstance(item, dict):
                    normalized.append(item)
                else:
                    print(
                        f"[ERROR] Invalid record type at index {idx} in {self.file_path}. "
                        "Expected an object."
                    )
            return normalized

        except json.JSONDecodeError as exc:
            print(f"[ERROR] Invalid JSON in file: {self.file_path}. {exc}")
            return []
        except OSError as exc:
            print(f"[ERROR] Unable to read file: {self.file_path}. {exc}")
            return []

    def write(self, records: List[dict]) -> None:
        if records is None:
            records = []

        if not isinstance(records, list):
            raise ValueError("records must be a list of dicts")

        for item in records:
            if not isinstance(item, dict):
                raise ValueError("records must be a list of dicts")

        directory = os.path.dirname(self.file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
        except OSError as exc:
            print(f"[ERROR] Unable to write file: {self.file_path}. {exc}")