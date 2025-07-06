#!/usr/bin/env python3
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


def get_results() -> None:
    query_path: Path = QUERY_DIR / "orders.graphql"
    query: str = query_path.read_text()
    result: JSONObject = json.loads(GraphQL().execute(query=query))
    for value in result["data"]["orders"]["edges"]:
        print(value["node"])


def main() -> None:
    with Session.temp(SHOP_URL, API_VERSION, environ["TOKEN"]):
        get_results()


if __name__ == "__main__":
    main()
