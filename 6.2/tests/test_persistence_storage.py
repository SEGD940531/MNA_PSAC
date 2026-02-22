import unittest
import tempfile
import os
import json

from persistence.storage_json import JSONStorage


class TestJSONStorage(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.tmp.name, "test.json")
        self.storage = JSONStorage(self.file_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_read_empty_file(self):
        data = self.storage.read()
        self.assertEqual(data, [])

    def test_write_and_read(self):
        records = [{"id": "1", "name": "test"}]
        self.storage.write(records)

        result = self.storage.read()
        self.assertEqual(result, records)

    def test_invalid_json_handled(self):
        with open(self.file_path, "w") as f:
            f.write("{ invalid json")

        data = self.storage.read()
        self.assertEqual(data, [])

    def test_file_not_exists(self):
        data = self.storage.read()
        self.assertEqual(data, [])

    def test_overwrite_data(self):
        self.storage.write([{"id": "1"}])
        self.storage.write([{"id": "2"}])

        result = self.storage.read()
        self.assertEqual(result[0]["id"], "2")