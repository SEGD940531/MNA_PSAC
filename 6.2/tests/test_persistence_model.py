import unittest
from persistence.model import BaseModel


class DummyModel(BaseModel):
    entity_name = "dummy"

    def __init__(self, id, name):
        super().__init__(id=id)
        self.name = name

    def validate(self):
        super().validate()
        if not self.name:
            raise ValueError("name required")


class TestBaseModel(unittest.TestCase):

    def test_to_dict(self):
        obj = DummyModel(id="1", name="test")
        result = obj.to_dict()
        self.assertEqual(result["id"], "1")
        self.assertEqual(result["name"], "test")

    def test_from_dict_valid(self):
        data = {"id": "1", "name": "test"}
        obj = DummyModel.from_dict(data)
        self.assertEqual(obj.id, "1")
        self.assertEqual(obj.name, "test")

    def test_validation_error(self):
        data = {"id": "1", "name": ""}
        with self.assertRaises(ValueError):
            DummyModel.from_dict(data)

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            DummyModel(id=None, name="test")