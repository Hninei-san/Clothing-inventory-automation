"""SQLite persistence for the Streamlit clothing inventory app."""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS = {
    "markup": 100.0,
    "currency": "USD",
    "rounding": ".99",
    "low_stock": 3,
}


def database_path() -> Path:
    return Path(os.environ.get("CLOTHING_DB_PATH", "clothing_inventory.db"))


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(database_path(), timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def connection():
    database = connect()
    try:
        yield database
        database.commit()
    except Exception:
        database.rollback()
        raise
    finally:
        database.close()


def initialize() -> None:
    with connection() as database:
        database.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                sku TEXT NOT NULL DEFAULT '',
                category TEXT NOT NULL DEFAULT 'Other',
                brand TEXT NOT NULL DEFAULT '',
                color TEXT NOT NULL DEFAULT '',
                size TEXT NOT NULL DEFAULT '',
                qty INTEGER NOT NULL DEFAULT 0,
                buy_price REAL NOT NULL DEFAULT 0,
                sell_price REAL NOT NULL DEFAULT 0,
                photo BLOB,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                qty INTEGER NOT NULL,
                price REAL NOT NULL,
                cost REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE RESTRICT
            );
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier TEXT NOT NULL DEFAULT '',
                date TEXT NOT NULL,
                total REAL NOT NULL DEFAULT 0,
                item_count INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        for key, value in DEFAULT_SETTINGS.items():
            database.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value)),
            )


def get_settings() -> dict[str, Any]:
    with connection() as database:
        saved = {row["key"]: row["value"] for row in database.execute("SELECT * FROM settings")}
    result: dict[str, Any] = {**DEFAULT_SETTINGS, **saved}
    result["markup"] = float(result["markup"])
    result["low_stock"] = int(result["low_stock"])
    return result


def save_settings(settings: dict[str, Any]) -> None:
    with connection() as database:
        database.executemany(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            [(key, str(value)) for key, value in settings.items()],
        )


def list_products() -> list[dict[str, Any]]:
    with connection() as database:
        rows = database.execute("SELECT * FROM products ORDER BY name COLLATE NOCASE").fetchall()
    return [dict(row) for row in rows]


def get_product(product_id: str) -> dict[str, Any] | None:
    with connection() as database:
        row = database.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return dict(row) if row else None


def save_product(product: dict[str, Any]) -> None:
    columns = (
        "id", "name", "sku", "category", "brand", "color", "size",
        "qty", "buy_price", "sell_price", "photo",
    )
    values = [product.get(column) for column in columns]
    with connection() as database:
        database.execute(
            f"INSERT INTO products ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)}) "
            "ON CONFLICT(id) DO UPDATE SET "
            "name=excluded.name, sku=excluded.sku, category=excluded.category, "
            "brand=excluded.brand, color=excluded.color, size=excluded.size, "
            "qty=excluded.qty, buy_price=excluded.buy_price, sell_price=excluded.sell_price, "
            "photo=COALESCE(excluded.photo, products.photo), updated_at=CURRENT_TIMESTAMP",
            values,
        )


def delete_product(product_id: str) -> None:
    with connection() as database:
        database.execute("DELETE FROM products WHERE id = ?", (product_id,))


def adjust_stock(product_id: str, change: int) -> int:
    with connection() as database:
        cursor = database.execute(
            "UPDATE products SET qty = MAX(0, qty + ?), updated_at=CURRENT_TIMESTAMP WHERE id = ?",
            (change, product_id),
        )
        if not cursor.rowcount:
            raise ValueError("Product not found.")
        return database.execute("SELECT qty FROM products WHERE id = ?", (product_id,)).fetchone()["qty"]


def record_sale(product_id: str, qty: int, price: float, sale_date: str) -> None:
    with connection() as database:
        product = database.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if not product:
            raise ValueError("Product not found.")
        if qty < 1 or qty > product["qty"]:
            raise ValueError("Sale quantity exceeds stock.")
        database.execute(
            "INSERT INTO sales (product_id, product_name, qty, price, cost, date) VALUES (?, ?, ?, ?, ?, ?)",
            (product_id, product["name"], qty, price, product["buy_price"], sale_date),
        )
        database.execute(
            "UPDATE products SET qty = qty - ?, updated_at=CURRENT_TIMESTAMP WHERE id = ?",
            (qty, product_id),
        )


def list_sales() -> list[dict[str, Any]]:
    with connection() as database:
        rows = database.execute("SELECT * FROM sales ORDER BY date DESC, id DESC").fetchall()
    return [dict(row) for row in rows]


def undo_sale(sale_id: int) -> None:
    with connection() as database:
        sale = database.execute("SELECT * FROM sales WHERE id = ?", (sale_id,)).fetchone()
        if not sale:
            raise ValueError("Sale not found.")
        database.execute(
            "UPDATE products SET qty = qty + ?, updated_at=CURRENT_TIMESTAMP WHERE id = ?",
            (sale["qty"], sale["product_id"]),
        )
        database.execute("DELETE FROM sales WHERE id = ?", (sale_id,))


def add_expense(description: str, amount: float, expense_date: str) -> None:
    with connection() as database:
        database.execute(
            "INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)",
            (description, amount, expense_date),
        )


def list_expenses() -> list[dict[str, Any]]:
    with connection() as database:
        rows = database.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC").fetchall()
    return [dict(row) for row in rows]


def delete_expense(expense_id: int) -> None:
    with connection() as database:
        database.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def add_receipt(supplier: str, receipt_date: str, total: float, item_count: int) -> None:
    with connection() as database:
        database.execute(
            "INSERT INTO receipts (supplier, date, total, item_count) VALUES (?, ?, ?, ?)",
            (supplier, receipt_date, total, item_count),
        )


def list_receipts() -> list[dict[str, Any]]:
    with connection() as database:
        rows = database.execute("SELECT * FROM receipts ORDER BY date DESC, id DESC").fetchall()
    return [dict(row) for row in rows]


def delete_receipt(receipt_id: int) -> None:
    with connection() as database:
        database.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
