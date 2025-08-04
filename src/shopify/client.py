from collections.abc import Iterator
from http.client import HTTPResponse
from pathlib import Path
from urllib.request import Request, urlopen
import json
import logging

from .responses import InventoryItem, Order
from type_definitions import JSONObject


class Client:
    API_VERSION: str = "2024-07"
    PAGE_SIZE: int = 10

    def __init__(
        self,
        query_dir: Path,
        merchant: str,
        token: str,
    ) -> None:
        self.query_dir = query_dir
        self.merchant = merchant
        self.token = token

    @property
    def query_dir(self) -> Path:
        return self._query_dir

    @query_dir.setter
    def query_dir(self, value: Path) -> None:
        logging.debug(f"Setting query_dir as {value}")
        self._query_dir: Path = value

    @property
    def merchant(self) -> str:
        return self._merchant

    @merchant.setter
    def merchant(self, value: str) -> None:
        logging.debug(f"Setting merchant as {value}")
        self._merchant: str = value

    @property
    def shop_url(self) -> str:
        return f"https://{self.merchant}.myshopify.com"

    @property
    def api_url(self) -> str:
        return f"{self.shop_url}/admin/api/unstable/graphql.json"

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        logging.debug(f"Setting token")
        self._token: str = value

    @property
    def API_HEADERS(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.token,
        }

    def query(self, query: str) -> str:
        path: Path = self.query_dir / f"{query}.graphql"
        return path.read_text()

    def _request(self, data: bytes) -> bytes:
        request: Request = Request(
            method="POST",
            url=self.api_url,
            headers=self.API_HEADERS,
            data=data,
        )
        response: HTTPResponse = urlopen(request)
        return response.read()

    def request(self, data: JSONObject) -> JSONObject:
        _data: bytes = json.dumps(data).encode()
        response_bytes: bytes = self._request(_data)
        response_string: str = response_bytes.decode()
        return json.loads(response_string)

    def get_inventory_items(
        self,
        latest: str | None = None,
    ) -> Iterator[InventoryItem]:
        variables: JSONObject = {"pageSize": Client.PAGE_SIZE}
        if latest:
            variables["query"] = f"created_at:>'{latest}'"
        data: JSONObject = {
            "query": self.query("inventory"),
            "variables": variables,
        }
        while True:
            response: JSONObject = self.request(data)
            inventory_items: JSONObject = response["data"]["inventoryItems"]
            for item in inventory_items["nodes"]:
                yield InventoryItem(item)
            page_info: JSONObject = inventory_items["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            data["variables"]["cursor"] = page_info["endCursor"]

    def get_orders(self, latest: str | None = None) -> Iterator[Order]:
        query: str = self.query("orders")
        variables: dict[str, int | str] = {"pageSize": Client.PAGE_SIZE}
        if latest is not None:
            variables["query"] = f"created_at:>'{latest}'"
        data: JSONObject = {
            "query": query,
            "variables": variables,
        }
        while True:
            response: JSONObject = self.request(data)
            orders: JSONObject = response["data"]["orders"]
            for order in orders["nodes"]:
                yield Order(order)
            page_info: JSONObject = orders["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            data["variables"]["cursor"] = page_info["endCursor"]
