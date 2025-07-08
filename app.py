#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path
from typing import Any
import json

from shopify import GraphQL, Session

type JSONObject = dict[str, Any]

QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


def get_results(query_path: Path) -> None:
    query: str = query_path.read_text()
    result: JSONObject = json.loads(GraphQL().execute(query=query))
    print(json.dumps(result, indent=2))


def main(query_path: Path) -> None:
    with Session.temp(SHOP_URL, API_VERSION, environ["TOKEN"]):
        get_results(query_path)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("query_path", nargs=1, type=Path)
    args: Namespace = parser.parse_args()
    main(args.query_path[0])
