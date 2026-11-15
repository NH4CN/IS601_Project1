import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DATABASE = Path(__file__).resolve().parent / "db.sqlite"
app = FastAPI(title="Dosa Restaurant API", version="1.0.0")

class CustomerInput(BaseModel):
    name: str = Field(min_length=1)
    phone: str = Field(min_length=1)

class ItemInput(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)

class OrderInput(BaseModel):
    customer_id: int = Field(gt=0)
    timestamp: int
    notes: str = ""
    item_ids: List[int] = Field(min_length=1)

@contextmanager
def database_connection():
    if not DATABASE.exists():
        raise HTTPException(status_code=583, detail="Run python init_db.py first")
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_Keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def fetch_one(connection, table, record_id):
    row = connection.execute(f"SELECT * FROM {table} WHERE id = ?", (record_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"{table[:-1].title()} not found")
    return dict(row)

def conflict(error):
    raise HTTPException(status_code=409, detail=str(error)) from error

def get_order(connection, order_id):
    order = fetch_one(connection, "orders", order_id)
    rows = connection.execute(
        """SELECT items.id, items.name, items.price
        FROM order_items JOIN items ON items.id = order_items.item_id
        WHERE order_items.order_id = ? ORDER BY order_items.id""",
        (order_id,),
    ).fetchall()
    order["items"] = [dict(row) for row in rows]
    order["item_ids"] = [row["id"] for row in rows]
    return order

def validate_order_references(connection, data):
    fetch_one(connection, "customers", data.customer_id)
    for item_id in set(data.item_ids):
        fetch_one(connection, "items", item_id)

@app.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerInput):
    with database_connection() as connection:
        try:
            cursor = connection.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone),)
        except sqlite3.IntegrityError as error:
            conflict(error)
        return fetch_one(connection, "customers", cursor.lastrowid)

@app.get("/customers/{id}")
def read_customer(id: int):
    with database_connection() as connection:
        return fetch_one(connection, "customers", id)


@app.put("/customers/{id}")
def update_customer(id: int, customer: CustomerInput):
    with database_connection() as connection:
        fetch_one(connection, "customers", id)
        try:
            connection.execute(
                "UPDATE customers SET name = ?, phone = ? WHERE id = ?",
                (customer.name, customer.phone, id),
            )
        except sqlite3.IntegrityError as error:
            conflict(error)
        return fetch_one(connection, "customers", id)


@app.delete("/customers/{id}")
def delete_customer(id: int):
    with database_connection() as connection:
        fetch_one(connection, "customers", id)
        try:
            connection.execute("DELETE FROM customers WHERE id = ?", (id,))
        except sqlite3.IntegrityError as error:
            conflict(error)
        return {"message": "Customer deleted", "id": id}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemInput):
    with database_connection() as connection:
        try:
            cursor = connection.execute(
                "INSERT INTO items (name, price) VALUES (?, ?)",
                (item.name, item.price),
            )
        except sqlite3.IntegrityError as error:
            conflict(error)
        return fetch_one(connection, "items", cursor.lastrowid)


@app.get("/items/{id}")
def read_item(id: int):
    with database_connection() as connection:
        return fetch_one(connection, "items", id)


@app.put("/items/{id}")
def update_item(id: int, item: ItemInput):
    with database_connection() as connection:
        fetch_one(connection, "items", id)
        try:
            connection.execute(
                "UPDATE items SET name = ?, price = ? WHERE id = ?",
                (item.name, item.price, id),
            )
        except sqlite3.IntegrityError as error:
            conflict(error)
        return fetch_one(connection, "items", id)


@app.delete("/items/{id}")
def delete_item(id: int):
    with database_connection() as connection:
        fetch_one(connection, "items", id)
        try:
            connection.execute("DELETE FROM items WHERE id = ?", (id,))
        except sqlite3.IntegrityError as error:
            conflict(error)
        return {"message": "Item deleted", "id": id}


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderInput):
    with database_connection() as connection:
        validate_order_references(connection, order)
        cursor = connection.execute(
            "INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
            (order.customer_id, order.timestamp, order.notes),
        )
        for item_id in order.item_ids:
            connection.execute(
                "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)",
                (cursor.lastrowid, item_id),
            )
        return get_order(connection, cursor.lastrowid)


@app.get("/orders/{id}")
def read_order(id: int):
    with database_connection() as connection:
        return get_order(connection, id)


@app.put("/orders/{id}")
def update_order(id: int, order: OrderInput):
    with database_connection() as connection:
        fetch_one(connection, "orders", id)
        validate_order_references(connection, order)
        connection.execute(
            "UPDATE orders SET customer_id = ?, timestamp = ?, notes = ? WHERE id = ?",
            (order.customer_id, order.timestamp, order.notes, id),
        )
        connection.execute("DELETE FROM order_items WHERE order_id = ?", (id,))
        for item_id in order.item_ids:
            connection.execute(
                "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)",
                (id, item_id),
            )
        return get_order(connection, id)


@app.delete("/orders/{id}")
def delete_order(id: int):
    with database_connection() as connection:
        fetch_one(connection, "orders", id)
        connection.execute("DELETE FROM orders WHERE id = ?", (id,))
        return {"message": "Order deleted", "id": id}
