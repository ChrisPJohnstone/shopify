from pathlib import Path
from sqlite3 import Connection, Cursor, connect
from typing import Any, Sequence
import logging

from shopify import InventoryItem, Order

type QueryParams = dict[str, Any] | Sequence[Any] | None


class Client:
    def __init__(self, query_dir: Path) -> None:
        self.query_dir = query_dir

    @property
    def DATABASE(self) -> Path:
        return Path.home() / ".shopify.db"

    @property
    def query_dir(self) -> Path:
        return self._query_dir

    @query_dir.setter
    def query_dir(self, value: Path) -> None:
        logging.debug(f"Setting query_dir as {value}")
        self._query_dir: Path = value

    def _execute(
        self,
        connection: Connection,
        query: str,
        params: QueryParams = None,
    ) -> list[tuple]:
        cursor: Cursor = connection.cursor()
        cursor.execute(query, params or {})
        output: list[tuple] = cursor.fetchall()
        if cursor.description:
            output.insert(
                0,
                tuple(description[0] for description in cursor.description),
            )
        cursor.close()
        connection.commit()
        return output

    def execute(self, query: str, params: QueryParams = None) -> list[tuple]:
        logging.debug(f"Executing {query} with {params}")
        with connect(self.DATABASE) as connection:
            return self._execute(connection, query, params)

    def query(self, query: str, query_type: str = "sql") -> str:
        path: Path = self.query_dir / f"{query}.{query_type}"
        return path.read_text()

    def create_table(self, table: str) -> None:
        ddl: str = self.query(table, "ddl")
        self.execute(ddl)

    def get_latest(self, table: str) -> str | None:
        self.create_table(f"{table}s")
        query: str = self.query(f"latest_{table}")
        return self.execute(query)[1][0]

    def add_inventory_item(self, item: InventoryItem) -> None:
        self.create_table("inventory_items")
        query: str = self.query("insert_inventory_item")
        params: dict[str, str | int | float] = {
            "id": item.id,
            "created_at": item.created_at,
            "variant_id": item.variant_id,
            "variant_name": item.variant_name,
            "variant_price": float(item.variant_price),
            "unit_cost": float(item.unit_cost),
            "stock": item.stock,
        }
        self.execute(query, params)

    def add_order(self, order: Order) -> None:
        self.create_table("orders")
        query: str = self.query("insert_order")
        for line_item in order.line_items:
            params: dict[str, str | float] = {
                "id": order.id,
                "created_at": order.created_at,
                "variant_id": line_item.variant_id,
                "variant_name": line_item.variant_name,
                "price": float(line_item.price),
                "discounted_price": float(line_item.discounted_price),
                "fees": float(order.fees),
            }
            self.execute(query, params)

    def get_orders(self) -> list[tuple]:
        query: str = self.query("orders")
        return self.execute(query)

    def delete_inventory_items(self) -> list[tuple]:
        query: str = self.query("delete_inventory_items")
        return self.execute(query)

    def get_inventory_items(self) -> list[tuple]:
        query: str = self.query("inventory_items")
        return self.execute(query)
