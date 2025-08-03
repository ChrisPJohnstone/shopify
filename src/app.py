#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path
import logging

from database import Client as DatabaseClient
from shopify_util import Client as ShopifyClient
from spreadsheet_util import write

QUERY_DIR: Path = Path("queries")
OUTPUT_PATH: Path = Path.home() / "Downloads" / "profit.ods"


class Controller:
    def __init__(
        self,
        database_client: DatabaseClient,
        shopify_client: ShopifyClient,
    ) -> None:
        self._database_client: DatabaseClient = database_client
        self._shopify_client: ShopifyClient = shopify_client

    def update_inventory_items(self) -> None:
        latest: str | None = self._database_client.get_latest("inventory_item")
        for item in self._shopify_client.get_inventory_items(latest):
            self._database_client.add_inventory_item(item)

    def update_orders(self) -> None:
        latest: str | None = self._database_client.get_latest("order")
        for order in self._shopify_client.get_orders(latest):
            self._database_client.add_order(order)

    def output(self) -> None:
        orders: list[tuple] = self._database_client.get_orders()
        write(OUTPUT_PATH, orders)


def main() -> None:
    database_client: DatabaseClient = DatabaseClient(QUERY_DIR / "sql")
    shopify_client: ShopifyClient = ShopifyClient(
        query_dir=QUERY_DIR / "graphql",
        merchant=environ["MERCHANT"],
        token=environ["TOKEN"],
    )
    controller: Controller = Controller(database_client, shopify_client)
    controller.update_inventory_items()
    controller.update_orders()
    controller.output()


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
