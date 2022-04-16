from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

from config import database
from configurations import ConfigurationsService
from equity import EquityService
from incomes.errors import IncomesError
from incomes.models import Income
from users import User, UsersService


class IncomesService:
    def __init__(self, account_id: int) -> None:
        self.__DATE_FROAMT = "%Y-%m-%d"
        self.__TABLE = "incomes"
        self._user: Optional[User] = UsersService.fetch_user(account_id)
        self._date: Optional[date] = None
        self._name: Optional[str] = None
        self._value: Optional[Decimal] = None

    def set_name(self, text: str = None) -> None:
        if text is None:
            raise IncomesError("Category is not selected")

        self._name = text

    def set_value(self, text: str = None) -> None:
        if text is None:
            raise IncomesError("Value is not added")

        try:
            self._value = Decimal(text.replace(",", "."))
        except InvalidOperation:
            raise IncomesError("Money value is invalid")

    def set_date(self, text: str = None) -> None:
        if text is None:
            raise IncomesError("Date is not selected")

        try:
            self._date = datetime.strptime(text, self.__DATE_FROAMT)
        except ValueError:
            raise IncomesError("Invalid date")

    def save_incomes(self):
        if not self._name or not self._date or not self._user:
            raise IncomesError("One or more mandatory values are not set")

        default_currency: str = ConfigurationsService.get_by_name("default_currency").value
        payload = {
            "name": self._name,
            "value": self._value,
            "currency": default_currency,
            "date": self._date,
            "user_id": self._user.id,
        }
        data: dict = database.insert(self.__TABLE, payload)
        instance = Income(**data)

        EquityService.update(instance)

        return instance

    def process_confirmation(self, text: Optional[str]) -> bool:
        if not text or "Yes" not in text:
            return False

        self.save_incomes()
        return True
