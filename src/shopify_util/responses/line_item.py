from ._base import Base
from type_definitions import JSONObject


class LineItem(Base):
    @property
    def id(self) -> str:
        return self._node["id"]

    @property
    def _variant(self) -> JSONObject:
        return self._node["variant"]

    @property
    def variant_id(self) -> str:
        full_id: str = self._variant["id"]
        last_slash_pos: int = full_id.rfind("/")
        return full_id[last_slash_pos + 1 :]
