#!/usr/bin/env python3
from os import environ
from pathlib import Path

from shopify_util import (
    Client as ShopifyClient,
    InventoryItem,
)


QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


def main() -> None:
    shopify_client: ShopifyClient = ShopifyClient(MERCHANT, environ["TOKEN"])
    inventory: list[InventoryItem] = shopify_client.get_inventory()
    for item in inventory:
        print(item)


if __name__ == "__main__":
    main()
