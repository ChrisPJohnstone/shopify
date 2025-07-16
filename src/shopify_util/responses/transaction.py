from decimal import Decimal

from ._base import Base
from type_definitions import JSONObject


class Transaction(Base):
    @property
    def _fees(self) -> list[JSONObject]:
        return self._node["fees"]

    @property
    def total_fees(self) -> Decimal:
        return Decimal(
            sum(Decimal(fee["amount"]["amount"]) for fee in self._fees)
        )
