#!/usr/bin/env python3
from dataclasses import dataclass
from os import environ
from pathlib import Path

from shopify_util import Client as ShopifyClient

QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


@dataclass
class Output:
    name: str
    price: int
    cost: int
    stock: int
    sales: int = 0


def main() -> None:
    client: ShopifyClient = ShopifyClient(MERCHANT, environ["TOKEN"])
    output: dict[str, Output] = {
        item.variant_id: Output(
            name=item.product,
            price=item.price,
            cost=item.cost,
            stock=item.stock,
            sales=0,
        )
        for item in client.get_inventory_items()
    }
    # TODO: Make TypedDict
    for order in client.get_orders():
        for line_item in order.line_items:
            output[line_item.variant_id].sales += 1
    for x in output.values():
        print(x)


if __name__ == "__main__":
    main()
