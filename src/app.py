#!/usr/bin/env python3
from os import environ
from pathlib import Path
import json

from shopify_util import Client as ShopifyClient
from type_definitions import JSONObject


QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


def main() -> None:
    shopify_client: ShopifyClient = ShopifyClient(MERCHANT, environ["TOKEN"])
    inventory: JSONObject = shopify_client.get_inventory()
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
