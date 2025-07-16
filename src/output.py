from decimal import Decimal
from textwrap import dedent

from type_definitions import JSONObject


class Output:
    def __init__(
        self,
        name: str,
        price: Decimal,
        cost: Decimal,
        stock: int,
    ) -> None:
        self._name: str = name
        self._price: Decimal = price
        self._cost: Decimal = cost
        self._stock: int = stock
        self._sales: int = 0

    def __str__(self) -> str:
        string: str = f"""
        Event: {self.name}
        - Price: {self.price:.2f}
        - Cost: {self.cost:.2f}
        - Stock: {self.stock}
        - Sales: {self.sales}
        - Profit: {self.profit:.2f}
        """
        return dedent(string).strip()

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def cost(self) -> Decimal:
        return self._cost

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def sales(self) -> int:
        return self._sales

    @sales.setter
    def sales(self, value: int) -> None:
        self._sales: int = value

    @property
    def profit_per_person(self) -> Decimal:
        return self.price - self.cost

    @property
    def profit(self) -> Decimal:
        return self.profit_per_person * self.sales

    @property
    def json_fields(self) -> list[str]:
        return [field for field in self.json.keys()]

    @property
    def json(self) -> JSONObject:
        return {
            "name": self.name,
            "price": f"{self.price:.2f}",
            "cost": f"{self.cost:.2f}",
            "stock": str(self.stock),
            "sales": str(self.sales),
            "profil": f"{self.profit:.2f}",
        }
