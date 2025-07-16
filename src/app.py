#!/usr/bin/env python3
from decimal import Decimal
from os import environ
from pathlib import Path
from textwrap import dedent

from shopify_util import Client as ShopifyClient

QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


class Output:
    def __init__(
        self,
        name: str,
        price: Decimal,
        cost: Decimal,
        stock: int,
    ) -> None:
        self._name: str = name
        self._price: Decimal = price
        self._cost: Decimal = cost
        self._stock: int = stock
        self._sales: int = 0

    def __str__(self) -> str:
        string: str = f"""
        Event: {self.name}
        - Price: {self.price:.2f}
        - Cost: {self.cost:.2f}
        - Stock: {self.stock}
        - Sales: {self.sales}
        - Profit: {self.profit:.2f}
        """
        return dedent(string).strip()

    def __repr__(self) -> str:
        properties: list[str] = [
            self.name,
            f"{self.price:.2f}",
            f"{self.cost:.2f}",
            str(self.stock),
            str(self.sales),
            f"{self.profit:.2f}",
        ]
        return "|".join(properties)

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def cost(self) -> Decimal:
        return self._cost

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def sales(self) -> int:
        return self._sales

    @sales.setter
    def sales(self, value: int) -> None:
        self._sales: int = value

    @property
    def profit_per_person(self) -> Decimal:
        return self.price - self.cost

    @property
    def profit(self) -> Decimal:
        return self.profit_per_person * self.sales


def main() -> None:
    client: ShopifyClient = ShopifyClient(MERCHANT, environ["TOKEN"])
    output: dict[str, Output] = {
        item.variant_id: Output(
            name=item.product,
            price=item.price,
            cost=item.cost,
            stock=item.stock,
        )
        for item in client.get_inventory_items()
    }
    for order in client.get_orders():
        for line_item in order.line_items:
            output[line_item.variant_id].sales += 1
    for x in output.values():
        print(x)


if __name__ == "__main__":
    main()
