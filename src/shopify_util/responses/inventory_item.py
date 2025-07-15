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
    def _variant(self) -> JSONObject:
        return self._node["variant"]

    @property
    def product(self) -> str:
        return self._variant["displayName"]

    @property
    def price(self) -> int:
        return self._variant["price"]

    @property
    def _unit_cost(self) -> JSONObject:
        return self._node["unitCost"]

    @property
    def cost(self) -> int:
        return self._unit_cost["amount"]

    @property
    def _inventory_levels(self) -> list[InventoryLevel]:
        return self.__inventory_levels

    @property
    def stock(self) -> int:
        return sum(level.available for level in self._inventory_levels)
