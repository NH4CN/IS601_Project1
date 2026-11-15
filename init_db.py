"""Initialize the Dosa Restaurant SQLite database from midterm JSON orders."""

import argparse
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "db.sqlite"

SCHEMA = """
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL CHECK (price >= 0)
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE RESTRICT
);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
"""


def initialize(input_file: Path, database: Path) -> None:
    """Recreate and populate a database using the provided orders file."""
    with input_file.open(encoding="utf-8") as handle:
        orders = json.load(handle)
    if not isinstance(orders, list):
        raise ValueError("Input JSON must be a list of orders")

    # Populate a temporary database first; don't destroy an existing DB on failure.
    temporary = database.with_name(database.name + ".tmp")
    temporary.unlink(missing_ok=True)
    try:
        with sqlite3.connect(temporary) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(SCHEMA)
            for order in orders:
                connection.execute(
                    "INSERT OR IGNORE INTO customers (name, phone) VALUES (?, ?)",
                    (order["name"], order["phone"]),
                )
                customer_id = connection.execute(
                    "SELECT id FROM customers WHERE phone = ?", (order["phone"],)
                ).fetchone()[0]
                cursor = connection.execute(
                    "INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
                    (customer_id, order["timestamp"], order.get("notes", "")),
                )
                order_id = cursor.lastrowid
                for item in order["items"]:
                    connection.execute(
                        "INSERT OR IGNORE INTO items (name, price) VALUES (?, ?)",
                        (item["name"], item["price"]),
                    )
                    item_id = connection.execute(
                        "SELECT id FROM items WHERE name = ?", (item["name"],)
                    ).fetchone()[0]
                    connection.execute(
                        "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)",
                        (order_id, item_id),
                    )
            connection.commit()
        temporary.replace(database)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    with sqlite3.connect(database) as connection:
        for table in ("customers", "items", "orders", "order_items"):
            count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count}")
    print(f"Database initialized: {database}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the Dosa database")
    parser.add_argument("input", nargs="?", default="example_orders.json")
    args = parser.parse_args()
    initialize(Path(args.input), DATABASE)


if __name__ == "__main__":
    main()
