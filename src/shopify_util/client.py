from pathlib import Path
import json
import logging

from shopify import GraphQL, Session

from type_definitions import JSONObject


class Client:
    QUERY_DIR: Path = Path("queries")
    API_VERSION: str = "2024-07"

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

    def _request(self, query: str) -> JSONObject:
        result: JSONObject = json.loads(GraphQL().execute(query=query))
        if "data" not in result:
            raise ValueError(json.dumps(result, indent=2))
        return result["data"]

    def request(self, query: str) -> JSONObject:
        with Session.temp(self.shop_url, Client.API_VERSION, self.token):
            return self._request(query)

    def get_inventory(self) -> JSONObject:
        output: JSONObject = {}
        query: str = self.query("inventory")
        return self.request(query)
