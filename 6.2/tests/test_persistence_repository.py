import os
import tempfile
import unittest
from dataclasses import dataclass

from persistence.model import BaseModel
from persistence.repository import Repository


@dataclass
class DummyModel(BaseModel):
    entity_name = "dummy"
    name: str = ""

    def validate(self) -> None:
        super().validate()
        if not self.name:
            raise ValueError("name required")


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.tmp.name, "dummy.json")
        self.repo = Repository(DummyModel, self.file_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_get(self):
        obj = DummyModel(id="1", name="test")
        self.repo.create(obj)

        result = self.repo.get("1")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "test")

    def test_get_all(self):
        self.repo.create(DummyModel(id="1", name="a"))
        self.repo.create(DummyModel(id="2", name="b"))

        results = self.repo.all()
        self.assertEqual(len(results), 2)

    def test_delete(self):
        self.repo.create(DummyModel(id="1", name="a"))
        self.repo.delete("1")

        result = self.repo.get("1")
        self.assertIsNone(result)

    def test_update(self):
        self.repo.create(DummyModel(id="1", name="a"))

        updated = DummyModel(id="1", name="updated")
        self.repo.update(updated)

        result = self.repo.get("1")
        self.assertEqual(result.name, "updated")

    def test_duplicate_id(self):
        self.repo.create(DummyModel(id="1", name="a"))

        with self.assertRaises(ValueError):
            self.repo.create(DummyModel(id="1", name="b"))

    def test_delete_non_existing(self):
        # should not crash
        self.repo.delete("999")

    def test_update_non_existing(self):
        with self.assertRaises(ValueError):
            self.repo.update(DummyModel(id="999", name="x"))

    def test_invalid_data_in_file(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("invalid json")

        results = self.repo.all()
        self.assertEqual(results, [])

    def test_validation_on_create(self):
        with self.assertRaises(ValueError):
            self.repo.create(DummyModel(id="1", name=""))
