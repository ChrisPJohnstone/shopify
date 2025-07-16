from decimal import Decimal

from ._base import Base
from .line_item import LineItem
from .transaction import Transaction


class Order(Base):
    def __post_init__(self) -> None:
        self._line_items: list[LineItem] = [
            LineItem(value) for value in self._node["lineItems"]["nodes"]
        ]
        self._transactions: list[Transaction] = [
            Transaction(value) for value in self._node["transactions"]
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

    @property
    def transactions(self) -> list[Transaction]:
        return self._transactions

    @property
    def fees(self) -> Decimal:
        return Decimal(sum(t.total_fees for t in self.transactions))
