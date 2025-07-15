#!/usr/bin/env python3
from os import environ
from pathlib import Path
import json

from shopify_util import (
    Client as ShopifyClient,
    InventoryItem,
)


QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


def main() -> None:
    client: ShopifyClient = ShopifyClient(MERCHANT, environ["TOKEN"])
    inventory: list[InventoryItem] = list(client.get_inventory_items())
    output: list[dict[str, str | int]] = []
    for item in inventory:
        product: dict[str, str | int] = {
            "name": item.product,
            "price": item.price,
            "cost": item.cost,
            "stock": item.stock,
        }
        output.append(product)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
