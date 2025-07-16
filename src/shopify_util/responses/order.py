from ._base import Base
from .line_item import LineItem
from type_definitions import JSONObject


class Order(Base):
    def __init__(self, value: JSONObject) -> None:
        super().__init__(value)
        self._line_items: list[LineItem] = [
            LineItem(value) for value in self._node["lineItems"]["nodes"]
        ]

    @property
    def id(self) -> str:
        return self._node["id"]

    @property
    def line_items(self) -> list[LineItem]:
        return self._line_items
