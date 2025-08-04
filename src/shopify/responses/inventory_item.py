from decimal import Decimal

from ._base import Base
from .inventory_level import InventoryLevel
from type_definitions import JSONObject


class InventoryItem(Base):
    def __post_init__(self) -> None:
        self.__inventory_levels: list[InventoryLevel] = [
            InventoryLevel(value)
            for value in self._node["inventoryLevels"]["nodes"]
        ]

    @property
    def id(self) -> str:
        return self._node["id"]

    @property
    def created_at(self) -> str:
        return self._node["createdAt"]

    @property
    def _variant(self) -> JSONObject:
        return self._node["variant"]

    @property
    def variant_id(self) -> str:
        full_id: str = self._variant["id"]
        last_slash_pos: int = full_id.rfind("/")
        return full_id[last_slash_pos + 1 :]

    @property
    def variant_name(self) -> str:
        return self._variant["displayName"]

    @property
    def variant_price(self) -> Decimal:
        return Decimal(self._variant["price"])

    @property
    def _unit_cost(self) -> JSONObject:
        if (cost := self._node["unitCost"]) is None:
            return {}
        return cost

    @property
    def unit_cost(self) -> Decimal:
        return Decimal(self._unit_cost.get("amount", 0))

    @property
    def _inventory_levels(self) -> list[InventoryLevel]:
        return self.__inventory_levels

    @property
    def stock(self) -> int:
        return sum(level.available for level in self._inventory_levels)
