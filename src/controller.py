#!/usr/bin/env python3
from collections.abc import Iterator
from pathlib import Path
import json

from shopify import Client as ShopifyClient, InventoryItem, Order


class Controller:
    def __init__(
        self,
        project_dir: Path | None = None,
    ) -> None:
        self.project_dir = project_dir
        env_config: dict[str, str] = self.env_config()
        self.shopify_client = ShopifyClient(
            query_dir=self.graphql_query_dir,
            merchant=env_config["Merchant"],
            token=env_config["Token"],
        )

    @property
    def project_dir(self) -> Path:
        return self._query_dir

    @project_dir.setter
    def project_dir(self, value: Path | None) -> None:
        self._query_dir: Path = value or Path.cwd()

    def env_config(self) -> dict[str, str]:
        filepath: Path = self.project_dir / "env.json"
        return json.loads(filepath.read_text())

    @property
    def query_dir(self) -> Path:
        return self._query_dir / "queries"

    @property
    def sql_query_dir(self) -> Path:
        return self.query_dir / "sql"

    @property
    def graphql_query_dir(self) -> Path:
        return self.query_dir / "graphql"

    @property
    def shopify_client(self) -> ShopifyClient:
        return self._shopify_client

    @shopify_client.setter
    def shopify_client(self, value: ShopifyClient) -> None:
        self._shopify_client: ShopifyClient = value

    def get_inventory_items(self) -> Iterator[InventoryItem]:
        yield from self.shopify_client.get_inventory_items()

    def get_orders(self) -> Iterator[Order]:
        yield from self.shopify_client.get_orders()
