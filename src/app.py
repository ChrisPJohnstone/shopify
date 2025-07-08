#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path

from shopify_util import Client as ShopifyClient


QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


def main(query_path: Path) -> None:
    shopify_client: ShopifyClient = ShopifyClient(MERCHANT, environ["TOKEN"])
    shopify_client.request(query_path)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("query_path", nargs=1, type=Path)
    args: Namespace = parser.parse_args()
    main(args.query_path[0])
