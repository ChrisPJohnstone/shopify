from ._base import Base
from type_definitions import JSONObject


class InventoryLevel(Base):
    @property
    def _quantities(self) -> JSONObject:
        return {
            quantity["name"]: quantity["quantity"]
            for quantity in self._node["quantities"]
        }

    @property
    def available(self) -> int:
        return self._quantities.get("available", 0)
