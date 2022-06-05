from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional, Union

from categories.domain import Category
from shared.domain import BaseError, Enum, Model, random_uuid
from storages import Storage


class CostsError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Adding costs error"
        super().__init__(message, *args, **kwargs)


class Cost(Model):
    id: int
    name: str
    value: Decimal
    currency: str
    date: date
    user_id: int
    category_id: int

    def __str__(self) -> str:
        return self.name

    def __add_costs_with_same_currency(self, other: Cost) -> Decimal:
        return self.value + other.value

    def __add_cost_and_decimal(self, other: Decimal) -> Decimal:
        return self.value + other

    def __add__(self, other: Union[Cost, Decimal, int]) -> Decimal:
        if isinstance(other, Cost) and other.currency == self.currency:
            return self.__add_costs_with_same_currency(other)
        elif isinstance(other, Cost) and other.currency is not self.currency:
            raise CostsError("It is not available to add costs with different currencies")
        elif isinstance(other, Decimal):
            return self.__add_cost_and_decimal(other)
        elif isinstance(other, int):
            return self.__add_cost_and_decimal(Decimal(str(other)))
        raise CostsError()

    def __radd__(self, other: Union[Cost, Decimal]) -> Decimal:
        return self.__add__(other)

    def __sub__(self, other: Union[Cost, Decimal]) -> Decimal:
        if isinstance(other, Cost):
            other.value = -other.value
        elif isinstance(other, Decimal):
            other = -other

        return self.__add__(other)

    def fdate(self, date_format="%Y-%m-%d") -> str:
        return self.date.strftime(date_format)


class CostsGeneralMenu(Enum):
    ADD_COST = "Add costs 💵"
    DELETE_COST = "Delete costs 💵"


class ExtraCallbackData(Enum):
    DEL_MONTH_SELECTED = random_uuid()
    ADD_MONTH_SELECTED = random_uuid()
    DEL_CATEGORY_SELECTED = random_uuid()
    ADD_CATEGORYADD_SELECTED = random_uuid()
    COST_ID_SELECTED = random_uuid()
    DEL_CONFIRMATION_SELECTED = random_uuid()
    ADD_CONFIRMATION_SELECTED = random_uuid()


class CostsStorage(Storage):
    __slots__ = "costs", "category", "delete_id", "value", "description", "date"

    def __init__(self, account_id: int) -> None:
        if getattr(self, "__initialized", False):
            return

        super().__init__(account_id)
        self.value: Optional[str] = None
        self.description: Optional[str] = None
        self.date: Optional[date] = None
        self.costs: Optional[list[Cost]] = None
        self.category: Optional[Category] = None
        self.delete_id: Optional[str] = None
