from ._base import Base
from type_definitions import JSONObject


class InventoryLevel(Base):
    @property
    def _quantities(self) -> list[JSONObject]:
        return self._node["quantities"]

    @property
    def available(self) -> int:
        if not hasattr(self, "_available"):
            self._available: int = self._sum_quantities("available")
        return self._available

    def _sum_quantities(self, name: str) -> int:
        return sum(filter(lambda x: x["name"] == name, self._quantities))
