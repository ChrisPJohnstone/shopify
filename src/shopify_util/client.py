from collections.abc import Iterable
from pathlib import Path
import json
import logging

from shopify import GraphQL, Session

from .responses import InventoryItem
from type_definitions import JSONObject


class Client:
    QUERY_DIR: Path = Path("queries")
    API_VERSION: str = "2024-07"
    PAGE_SIZE: int = 10

    def __init__(self, merchant: str, token: str) -> None:
        self.merchant = merchant
        self.token = token

    @property
    def merchant(self) -> str:
        return self._merchant

    @merchant.setter
    def merchant(self, value: str) -> None:
        logging.debug(f"Setting merchant as {value}")
        self._merchant: str = value

    @property
    def shop_url(self) -> str:
        return f"{self.merchant}.myshopify.com"

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        logging.debug(f"Setting token as {value}")
        self._token: str = value

    def query(self, query: str) -> str:
        path: Path = Client.QUERY_DIR / f"{query}.graphql"
        return path.read_text()

    def _request(self, query: str, **kwargs) -> JSONObject:
        result_string: str = GraphQL().execute(query=query, **kwargs)
        result: JSONObject = json.loads(result_string)
        if "data" not in result:
            raise ValueError(json.dumps(result, indent=2))
        return result["data"]

    def request(self, query: str, **kwargs) -> JSONObject:
        with Session.temp(self.shop_url, Client.API_VERSION, self.token):
            return self._request(query, **kwargs)

    def get_inventory_item(self, item_id: str) -> InventoryItem:
        query: str = self.query("inventory")
        response: JSONObject = self.request(
            query=query,
            operation_name="InventoryItem",
            variables={"id": item_id},
        )
        return InventoryItem(response)

    def get_inventory_items(self) -> Iterable[InventoryItem]:
        query: str = self.query("inventory")
        variables: dict[str, int | str] = {"pageSize": Client.PAGE_SIZE}
        while True:
            response: JSONObject = self.request(
                query=query,
                operation_name="InventoryItems",
                variables=variables,
            )
            inventory_items: JSONObject = response["inventoryItems"]
            for item in inventory_items["nodes"]:
                yield self.get_inventory_item(item["id"])
            page_info: JSONObject = inventory_items["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            variables["cursor"] = page_info["endCursor"]

    def get_orders_of_inventory_item(
        self,
        variant_id: str,
    ) -> Iterable[JSONObject]:
        query: str = self.query("orders")
        variables: dict[str, int | str] = {
            "variantQuery": f"line_items.variant_id:{variant_id}",
            "pageSize": Client.PAGE_SIZE,
        }
        while True:
            response: JSONObject = self.request(query, variables=variables)
            orders: JSONObject = response["orders"]
            for order in orders["nodes"]:
                yield order
                # TODO: Make response object
            page_info: JSONObject = orders["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            variables["cursor"] = page_info["endCursor"]
            quit()
