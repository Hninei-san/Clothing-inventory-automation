import os
import tempfile
import unittest
from pathlib import Path

import inventory_store as store


class InventoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.previous_path = os.environ.get("CLOTHING_DB_PATH")
        os.environ["CLOTHING_DB_PATH"] = str(Path(self.temp_dir.name) / "test.db")
        store.initialize()

    def tearDown(self):
        if self.previous_path is None:
            os.environ.pop("CLOTHING_DB_PATH", None)
        else:
            os.environ["CLOTHING_DB_PATH"] = self.previous_path
        self.temp_dir.cleanup()

    def test_product_photo_is_preserved_when_edit_does_not_upload_a_new_one(self):
        product = {
            "id": "dress-1",
            "name": "Summer dress",
            "sku": "D-1",
            "category": "Dresses",
            "brand": "Studio",
            "color": "Pink",
            "size": "S",
            "qty": 4,
            "buy_price": 10.0,
            "sell_price": 20.0,
            "photo": b"test-image",
        }
        store.save_product(product)
        store.save_product({**product, "qty": 5, "photo": None})

        saved = store.get_product("dress-1")
        self.assertEqual(saved["qty"], 5)
        self.assertEqual(saved["photo"], b"test-image")

    def test_sale_reduces_stock_and_undo_restores_it(self):
        store.save_product({
            "id": "tee-1",
            "name": "Cotton tee",
            "sku": "",
            "category": "Tops",
            "brand": "",
            "color": "White",
            "size": "M",
            "qty": 3,
            "buy_price": 5,
            "sell_price": 12,
            "photo": None,
        })

        store.record_sale("tee-1", 2, 12, "2026-10-13")
        self.assertEqual(store.get_product("tee-1")["qty"], 1)
        sale = store.list_sales()[0]
        self.assertEqual(sale["qty"], 2)
        store.undo_sale(sale["id"])
        self.assertEqual(store.get_product("tee-1")["qty"], 3)
        self.assertEqual(store.list_sales(), [])

    def test_settings_round_trip(self):
        store.save_settings({"currency": "EUR", "low_stock": 5})
        saved = store.get_settings()
        self.assertEqual(saved["currency"], "EUR")
        self.assertEqual(saved["low_stock"], 5)
        self.assertEqual(saved["markup"], store.DEFAULT_SETTINGS["markup"])


if __name__ == "__main__":
    unittest.main()
