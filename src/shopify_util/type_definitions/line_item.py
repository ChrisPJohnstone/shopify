from typing import TypedDict

from .variant import Variant


class LineItem(TypedDict):
    id: str
    variant: Variant
