import calendar
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Optional

from db import database
from equity import EquityCRUD
from finances import Currencies, Operations
from incomes.domain import Income, IncomesError, SalaryAnswers
from incomes.messages import (
    DATE_INVALID_ERROR,
    DATE_NOT_SELECTED_ERROR,
    INCOME_DETAILED_ITEM_MESSAGE,
    INCOME_GET_NO_USER_ERROR,
    INCOME_OPTION_INVALID_ERROR,
    INCOME_SAVE_ERROR,
    INCOME_TYPE_NOT_SELECTED_ERROR,
    MONEY_VALUE_INVALID_ERROR,
    MONTHLY_DATE_FORMAT_INVALID,
    TOTAL_INCOMES_LIST_MESSAGE,
    VALUE_NOT_ADDED_ERROR,
    YEAR_FORMAT_INVALID,
)
from shared.formatting import get_number_in_frames
from shared.messages import CATEGORY_NOT_SELECTED_ERROR, CURRENCY_INVALID_ERROR
from users import User, UsersCRUD


class IncomesService:
    __DATE_FROAMT = "%Y-%m-%d"
    __MONTHLY_DATE_FROAMT = "%Y-%m"
    __TABLE = "incomes"

    def __init__(self, account_id: int) -> None:
        self._user: Optional[User] = UsersCRUD.fetch_by_account_id(account_id)
        self._date: Optional[date] = None
        self._name: Optional[str] = None
        self._value: Optional[Decimal] = None
        self._currency: Optional[str] = None
        self._salary: Optional[bool] = None

    def set_salary(self, text: Optional[str] = None) -> None:
        if text is None:
            raise IncomesError(INCOME_TYPE_NOT_SELECTED_ERROR)
        if text not in SalaryAnswers.values():
            raise IncomesError(INCOME_OPTION_INVALID_ERROR)

        if text == SalaryAnswers.SALARY.value:
            self._salary = True
        elif text == SalaryAnswers.NOT_SALARY.value:
            self._salary = False

    def set_name(self, text: Optional[str] = None) -> None:
        if text is None:
            raise IncomesError(CATEGORY_NOT_SELECTED_ERROR)

        self._name = text

    def set_currency(self, text: Optional[str] = None) -> None:
        if text is None:
            raise IncomesError(VALUE_NOT_ADDED_ERROR)

        if text not in Currencies.values():
            raise IncomesError(CURRENCY_INVALID_ERROR.format(allowed=Currencies.get_database_values()))

        self._currency = Currencies.get_database_value(text)

    def set_value(self, text: Optional[str] = None) -> None:
        if text is None:
            raise IncomesError(VALUE_NOT_ADDED_ERROR)

        try:
            self._value = Decimal(text.replace(",", "."))
        except InvalidOperation:
            raise IncomesError(MONEY_VALUE_INVALID_ERROR)

    def set_date(self, text: Optional[str] = None) -> None:
        if text is None:
            raise IncomesError(DATE_NOT_SELECTED_ERROR)

        try:
            self._date = datetime.strptime(text, self.__DATE_FROAMT)
        except ValueError:
            raise IncomesError(DATE_INVALID_ERROR)

    def save_incomes(self):
        if not self._name or not self._date or not self._user or not self._value or not self._currency:
            raise IncomesError(INCOME_SAVE_ERROR)

        payload = {
            "name": self._name,
            "value": self._value,
            "currency": self._currency,
            "salary": self._salary,
            "date": self._date,
            "user_id": self._user.id,
        }
        data: dict = database.insert(self.__TABLE, payload)
        income = Income(**data)

        EquityCRUD.update(
            operation=Operations.ADD,
            value=income.value,
            currency=income.currency,
        )

        return income

    def process_confirmation(self, text: Optional[str]) -> bool:
        if not text or "Yes" not in text:
            return False

        self.save_incomes()
        return True

    @classmethod
    def get_detailed_incomes_message(cls, cached_users: dict[int, User], incomes: Optional[list[Income]]) -> str:
        """Return costs by category in readable format"""

        if not incomes:
            return ""

        result = ""

        for income in incomes:
            user: Optional[User] = cached_users.get(income.user_id) or UsersCRUD.fetch_by_id(income.user_id)

            if not user:
                raise IncomesError(INCOME_GET_NO_USER_ERROR.format(income=income))

            if user.account_id not in cached_users:
                cached_users[user.account_id] = user

            sign = "$" if income.currency == Currencies.get_database_value("USD") else ""
            fdate = income.date.strftime("%d")

            result += INCOME_DETAILED_ITEM_MESSAGE.format(
                fdate=fdate, user=user.full_name, income_name=income.name, income_value=income.value, sign=sign
            )

        return result

    @classmethod
    def get_formatted_incomes(cls, incomes: Optional[list[Income]], title="Total incomes") -> str:
        if not incomes:
            return ""

        total_incomes: Decimal = sum(incomes)  # type: ignore

        try:
            sign = "$" if incomes[0].currency == Currencies.get_database_value("USD") else ""
        except KeyError:
            sign = ""

        return TOTAL_INCOMES_LIST_MESSAGE.format(
            title=title, total_incomes=get_number_in_frames(total_incomes), sign=sign
        )

    @classmethod
    def get_incomes_by_currency(cls, costs: list[Income]) -> Iterable:
        attr = "currency"
        return groupby(sorted(costs, key=attrgetter(attr)), key=attrgetter(attr))

    @classmethod
    def get_monthly_incomes(cls, date: str) -> dict[str, list[Income]]:
        """
        Return the list of costs for the specific month by currency.
        Used mostly for analytics.
        date: str -- date in format YEAR-MONTH and
        """
        try:
            datetime.strptime(date, cls.__MONTHLY_DATE_FROAMT)
        except ValueError:
            raise IncomesError(MONTHLY_DATE_FORMAT_INVALID)

        year, month = date.split("-")
        _, last_day = calendar.monthrange(int(year), int(month))

        start_date = "-".join((date, "01"))
        end_date = "-".join((date, str(last_day)))

        q = f"SELECT * from {cls.__TABLE} WHERE date >='{start_date}' and date <= '{end_date}' ORDER BY date ASC"
        data = database.raw_execute(q)
        incomes = [Income(**item) for item in data]

        results = {currency: list(incomes_iter) for currency, incomes_iter in cls.get_incomes_by_currency(incomes)}

        return results

    @classmethod
    def get_annually_incomes(cls, year: str) -> dict[str, list[Income]]:
        """
        Return the list of incomes for the specific year by currency.
        Used mostly for analytics.
        """
        try:
            year_num = int(year)
        except ValueError:
            raise IncomesError(YEAR_FORMAT_INVALID)

        start_year = f"{year_num}-01-01"
        end_year = f"{year_num + 1}-01-01"
        q = f"SELECT * from {cls.__TABLE} WHERE date >='{start_year}' and date < '{end_year}' ORDER BY date ASC"
        data = database.raw_execute(q)
        incomes = [Income(**item) for item in data]

        return {currency: list(incomes_iter) for currency, incomes_iter in cls.get_incomes_by_currency(incomes)}
