import calendar
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Optional

from config import database
from configurations import ConfigurationsService
from costs.errors import CostsError
from costs.models import Category, Cost
from equity.services import EquityService
from users.models import User
from users.services import UsersService


class CategoriesCache(type):
    CATEGORIES_TABLE = "categories"

    @classmethod
    def get_categories(cls) -> list[Category]:
        data = [Category(**item) for item in database.fetchall(cls.CATEGORIES_TABLE)]
        return data

    def __getattr__(cls, attr):
        if attr == "CACHED_CATEGORIES":
            data = cls.get_categories()
            setattr(cls, attr, data)
            return data
        raise AttributeError(attr)


class CategoriesService(metaclass=CategoriesCache):
    CACHED_CATEGORIES: list[Category]

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Category]:
        for category in cls.CACHED_CATEGORIES:
            if category.name == name:
                return category
        return None


class CostsService:
    __DATE_FROAMT = "%Y-%m-%d"
    __MONTHLY_DATE_FROAMT = "%Y-%m"
    __COSTS_TABLE = "costs"

    def __init__(self, account_id: int) -> None:
        self.__DATE_FROAMT = "%Y-%m-%d"
        self.__MONTHLY_DATE_FROAMT = "%Y-%m"
        self.__COSTS_TABLE = "costs"
        self._user: Optional[User] = UsersService.fetch_by_account_id(account_id)
        self._category: Optional[Category] = None
        self._date: Optional[date] = None
        self._text: Optional[str] = None
        self._value: Optional[Decimal] = None

    def set_category(self, text: str = None) -> None:
        if text is None:
            raise CostsError("Category is not selected")

        if text not in {c.name for c in CategoriesService.CACHED_CATEGORIES}:
            raise CostsError("Category is not allowed")

        self._category = CategoriesService.get_by_name(text)

    def set_date(self, text: str = None) -> None:
        if text is None:
            raise CostsError("Date is not selected")

        try:
            self._date = datetime.strptime(text, self.__DATE_FROAMT)
        except ValueError:
            raise CostsError("Invalid date")

    def add_text(self, text: str = None) -> None:
        if text is None:
            raise CostsError("Text is not added")

        self._text = text

    def add_value(self, text: str = None) -> None:
        if text is None:
            raise CostsError("Value is not added")

        try:
            self._value = Decimal(text.replace(",", "."))
        except InvalidOperation:
            raise CostsError("Money value is invalid")

    def save_costs(self) -> Cost:
        if not self._text or not self._date or not self._category or not self._user:
            raise CostsError("One or more mandatory values are not set")

        default_currency: str = ConfigurationsService.get_by_name("default_currency").value

        payload = {
            "name": self._text,
            "value": self._value,
            "currency": default_currency,
            "date": self._date,
            "user_id": self._user.id,
            "category_id": self._category.id,
        }
        data: dict = database.insert(self.__COSTS_TABLE, payload)
        costs = Cost(**data)

        EquityService.update(costs)

        return Cost(**data)

    def process_confirmation(self, text: Optional[str]) -> bool:
        if not text or "Yes" not in text:
            return False

        self.save_costs()
        return True

    @classmethod
    def get_costs_by_currency(cls, costs: list[Cost]) -> Iterable:
        attr = "currency"
        return groupby(sorted(costs, key=attrgetter(attr)), key=attrgetter(attr))

    @classmethod
    def get_monthly_costs(cls, date: str) -> dict[str, list[Cost]]:
        """
        Return the list of costs for the specific month by currency.
        Used mostly for analytics.
        date: str -- date in format YEAR-MONTH and
        """
        try:
            datetime.strptime(date, cls.__MONTHLY_DATE_FROAMT)
        except ValueError:
            raise CostsError("Invalid monthly date format")

        year, month = date.split("-")
        _, last_day = calendar.monthrange(int(year), int(month))

        start_date = "-".join((date, "01"))
        end_date = "-".join((date, str(last_day)))

        q = f"SELECT * from {cls.__COSTS_TABLE} WHERE date >='{start_date}' and date <= '{end_date}' ORDER BY date ASC"
        data = database.raw_execute(q)
        costs = [Cost(**item) for item in data]

        return {currency: list(costs_iter) for currency, costs_iter in cls.get_costs_by_currency(costs)}
