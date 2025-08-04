from decimal import Decimal

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

    @property
    def variant_name(self) -> str:
        return self._variant["displayName"]

    @property
    def _original_total_set(self) -> JSONObject:
        return self._node["originalTotalSet"]

    @property
    def price(self) -> Decimal:
        return self._original_total_set["presentmentMoney"]["amount"]

    @property
    def _discounted_unit_price(self) -> JSONObject:
        return self._node["discountedUnitPriceAfterAllDiscountsSet"]

    @property
    def discounted_price(self) -> Decimal:
        return self._discounted_unit_price["presentmentMoney"]["amount"]
