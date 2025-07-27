#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path
import logging

from pandas import DataFrame

from shopify_util import Client as ShopifyClient
from database import Client as DatabaseClient

QUERY_DIR: Path = Path("queries")
OUTPUT_PATH: Path = Path.home() / "Downloads" / "profit.xlsx"


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

    def get_profit(self) -> DataFrame:
        records: list[tuple] = self._database_client.get_profit()
        df: DataFrame = DataFrame.from_records(records)
        df.columns = df.iloc[0]
        df: DataFrame = df[1:]  # type: ignore
        deduction_cols = df[["cost", "discounts", "fees"]]
        df["total_deductions"] = deduction_cols.sum(axis=1)
        df["before_tax"] = df["gross"] - df["total_deductions"]
        df["tax"] = df["before_tax"] * 0.2
        df["net"] = df["before_tax"] - df["tax"]
        df.drop("before_tax", axis=1)
        return df


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
    profit: DataFrame = controller.get_profit()
    profit.to_excel(OUTPUT_PATH)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
