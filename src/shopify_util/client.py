from pathlib import Path
import json
import logging

from type_definitions import JSONObject

from shopify import GraphQL, Session


class Client:
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

    def _request(self, query_path: Path) -> None:
        query: str = query_path.read_text()
        result: JSONObject = json.loads(GraphQL().execute(query=query))
        print(json.dumps(result, indent=2))

    def request(self, query_path: Path) -> None:
        with Session.temp(self.shop_url, Client.API_VERSION, self.token):
            self._request(query_path)
