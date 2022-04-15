from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

from config import database
from configurations import ConfigurationsService
from costs.errors import CostsError
from costs.models import Category, Cost
from users.models import User
from users.services import UsersService


class CategoriesCache(type):
    CATEGORIES_TABLE = "categories"

    @classmethod
    def get_categories(cls) -> list[Category]:
        return [Category(**item) for item in database.fetchall(cls.CATEGORIES_TABLE)]

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
    def __init__(self, account_id: int) -> None:
        self.__DATE_FROAMT = "%Y-%m-%d"
        self.__COSTS_TABLE = "costs"
        self._user: Optional[User] = UsersService.fetch_user(account_id)
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
            self._value = Decimal(text)
        except InvalidOperation:
            raise CostsError("Money value is invalid")

    def save_costs(self) -> Cost:
        if not self._text or not self._date or not self._category or not self._user or not self._category:
            raise CostsError("One or more mandatory values are not set")

        currency: str = ConfigurationsService.get_by_name("default_currency").value
        payload = {
            "name": self._text,
            "value": self._value,
            "currency": currency,
            "date": self._date,
            "user_id": self._user.id,
            "category_id": self._category.id,
        }
        data: dict = database.insert(self.__COSTS_TABLE, payload)

        return Cost(**data)

    def process_confirmation(self, text: Optional[str]) -> bool:
        if not text or "Yes" not in text:
            return False

        self.save_costs()
        return True
