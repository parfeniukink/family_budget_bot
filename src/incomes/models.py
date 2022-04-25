from datetime import date
from decimal import Decimal
from typing import Union

from incomes.errors import IncomesError
from shared.collections import Enum, Model


class SalaryAnswers(Enum):
    SALARY = "✅ Salary"
    NOT_SALARY = "❌ Not salary"


class Income(Model):
    id: int
    name: str
    value: Decimal
    currency: str
    salary: bool
    date: date
    user_id: int

    def __str__(self) -> str:
        return self.name

    def __add_incomes_with_same_currency(self, other: "Income") -> Decimal:
        return self.value + other.value

    def __add_income_and_decimal(self, other: Decimal) -> Decimal:
        return self.value + other

    def __add__(self, other: Union["Income", Decimal, int]) -> Decimal:
        if isinstance(other, Income) and other.currency == self.currency:
            return self.__add_incomes_with_same_currency(other)
        elif isinstance(other, Income) and other.currency is not self.currency:
            raise IncomesError("It is not available to add incomes with different currencies")
        elif isinstance(other, Decimal):
            return self.__add_income_and_decimal(other)
        elif isinstance(other, int):
            return self.__add_income_and_decimal(Decimal(str(other)))
        raise IncomesError()

    def __radd__(self, other: Union["Income", Decimal]) -> Decimal:
        return self.__add__(other)

    def __sub__(self, other: Union["Income", Decimal]) -> Decimal:
        if isinstance(other, Income):
            other.value = -other.value
        elif isinstance(other, Decimal):
            other = -other

        return self.__add__(other)
