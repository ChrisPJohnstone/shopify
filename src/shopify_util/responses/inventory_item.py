from ._base import Base
from .inventory_level import InventoryLevel
from type_definitions import JSONObject


class InventoryItem(Base):
    def __init__(self, value: JSONObject) -> None:
        super().__init__(value)
        self.__inventory_levels: list[InventoryLevel] = [
            InventoryLevel(value)
            for value in self._inventory_item["inventoryLevels"]["nodes"]
        ]

    @property
    def _inventory_item(self) -> JSONObject:
        return self._node["inventoryItem"]

    @property
    def _variant(self) -> JSONObject:
        return self._inventory_item["variant"]

    @property
    def variant_id(self) -> str:
        full_id: str = self._variant["id"]
        last_slash_pos: int = full_id.rfind("/")
        return full_id[last_slash_pos + 1 :]

    @property
    def product(self) -> str:
        return self._variant["displayName"]

    @property
    def price(self) -> int:
        return self._variant["price"]

    @property
    def _unit_cost(self) -> JSONObject:
        if (cost := self._inventory_item["unitCost"]) is None:
            return {}
        return cost

    @property
    def cost(self) -> int:
        return self._unit_cost.get("amount", 0)

    @property
    def _inventory_levels(self) -> list[InventoryLevel]:
        return self.__inventory_levels

    @property
    def stock(self) -> int:
        return sum(level.available for level in self._inventory_levels)
