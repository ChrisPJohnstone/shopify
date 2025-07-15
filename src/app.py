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
        sold: int = len(
            list(client.get_orders_of_inventory_item(item.variant_id))
        )
        """
        TODO: Fix sold number, the entire approach is based on a lie told by
        the AI assistant on shopify docs. You can't filter orders by variant
        so it looks like the only option is to pull all orders and assign them.
        """
        product: dict[str, str | int] = {
            "name": item.product,
            "price": item.price,
            "cost": item.cost,
            "stock": item.stock,
            "sold": sold,
        }
        output.append(product)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
