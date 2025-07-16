from ._base import Base
from .line_item import LineItem


class Order(Base):
    def __post_init__(self) -> None:
        self._line_items: list[LineItem] = [
            LineItem(value) for value in self._node["lineItems"]["nodes"]
        ]

    @property
    def id(self) -> str:
        return self._node["id"]

    @property
    def created_at(self) -> str:
        return self._node["createdAt"]

    @property
    def line_items(self) -> list[LineItem]:
        return self._line_items
