from typing import TypedDict

from .line_item import LineItem


class Order(TypedDict):
    id: str
    createdAt: str
    lineItems: list[LineItem]
