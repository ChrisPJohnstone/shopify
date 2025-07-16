#!/usr/bin/env python3
from csv import DictWriter
from os import environ
from pathlib import Path

from output import Output
from shopify_util import Client as ShopifyClient

QUERY_DIR: Path = Path("queries")
MERCHANT: str = environ["MERCHANT"]
SHOP_URL: str = f"{MERCHANT}.myshopify.com"
API_VERSION: str = "2024-07"


def write_to_csv(rows: list[Output]) -> None:
    with open("test.csv", "w") as file:
        writer: DictWriter = DictWriter(
            f=file,
            fieldnames=rows[0].json_fields,
        )
        writer.writeheader()
        writer.writerows([row.json for row in rows])


def main() -> None:
    shopify_client: ShopifyClient = ShopifyClient(
        query_dir=QUERY_DIR / "graphql",
        merchant=MERCHANT,
        token=environ["TOKEN"],
    )
    output: dict[str, Output] = {
        item.variant_id: Output(
            name=item.product,
            price=item.price,
            cost=item.cost,
            stock=item.stock,
        )
        for item in shopify_client.get_inventory_items()
    }
    for order in shopify_client.get_orders():
        for line_item in order.line_items:
            output[line_item.variant_id].sales += 1
    write_to_csv([v for v in output.values()])


if __name__ == "__main__":
    main()
