import os
import shutil
import tempfile
import unittest
from datetime import datetime

from reservation import Customer, Hotel, ReservationService


class TestReservationService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = os.path.join(self.tmp.name, "store_test", ts)
        os.makedirs(self.base_dir, exist_ok=True)

        self.svc = ReservationService(base_dir=self.base_dir)

        ok_hotel = self.svc.create_hotel(
            Hotel(
                id="h1",
                name="Hotel A",
                location="City",
                total_rooms=3,
                available_rooms=3,
            )
        )
        self.assertTrue(ok_hotel)

        ok_customer = self.svc.create_customer(
            Customer(
                id="c1",
                name="Alice",
                email="alice@example.com",
            )
        )
        self.assertTrue(ok_customer)

    def tearDown(self):
        if os.getenv("CLEAN_STORE_TEST") == "1":
            shutil.rmtree(self.base_dir, ignore_errors=True)
        self.tmp.cleanup()

    def test_create_and_display_hotel(self):
        info = self.svc.display_hotel("h1")
        self.assertIsNotNone(info)
        self.assertEqual(info["id"], "h1")
        self.assertEqual(info["total_rooms"], 3)

    def test_update_hotel(self):
        self.assertTrue(
            self.svc.update_hotel(
                "h1",
                name="Hotel Updated",
                total_rooms=5,
                available_rooms=5,
            )
        )
        info = self.svc.display_hotel("h1")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "Hotel Updated")
        self.assertEqual(info["available_rooms"], 5)

    def test_delete_hotel(self):
        self.assertTrue(self.svc.delete_hotel("h1"))
        self.assertIsNone(self.svc.get_hotel("h1"))

    def test_create_and_display_customer(self):
        info = self.svc.display_customer("c1")
        self.assertIsNotNone(info)
        self.assertEqual(info["email"], "alice@example.com")

    def test_update_customer(self):
        self.assertTrue(self.svc.update_customer("c1", name="Alice B"))
        info = self.svc.display_customer("c1")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "Alice B")

    def test_delete_customer(self):
        self.assertTrue(self.svc.delete_customer("c1"))
        self.assertIsNone(self.svc.get_customer("c1"))

    def test_create_reservation_decrements_rooms(self):
        res = self.svc.create_reservation(customer_id="c1", hotel_id="h1", rooms=2)
        self.assertIsNotNone(res)

        hotel = self.svc.get_hotel("h1")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.available_rooms, 1)

    def test_cancel_reservation_restores_rooms(self):
        res = self.svc.create_reservation(customer_id="c1", hotel_id="h1", rooms=2)
        self.assertIsNotNone(res)

        ok = self.svc.cancel_reservation(res.id)
        self.assertTrue(ok)

        hotel = self.svc.get_hotel("h1")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.available_rooms, 3)

        stored = self.svc.get_reservation(res.id)
        self.assertIsNotNone(stored)
        self.assertEqual(stored.status, "canceled")
        self.assertTrue(isinstance(stored.canceled_at, str) and stored.canceled_at.strip())

    def test_create_reservation_not_enough_rooms(self):
        res = self.svc.create_reservation(customer_id="c1", hotel_id="h1", rooms=99)
        self.assertIsNone(res)

    def test_create_reservation_missing_customer(self):
        res = self.svc.create_reservation(customer_id="missing", hotel_id="h1", rooms=1)
        self.assertIsNone(res)

    def test_create_reservation_missing_hotel(self):
        res = self.svc.create_reservation(customer_id="c1", hotel_id="missing", rooms=1)
        self.assertIsNone(res)

    def test_cancel_non_existing_reservation(self):
        ok = self.svc.cancel_reservation("missing")
        self.assertFalse(ok)

    def test_invalid_json_files_do_not_crash(self):
        # Corrupt the exact file used by the service repository.
        hotels_file = getattr(self.svc.hotels.storage, "file_path", "")
        self.assertTrue(isinstance(hotels_file, str) and hotels_file)

        with open(hotels_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json")

        hotels = self.svc.hotels.all()
        self.assertEqual(hotels, [])