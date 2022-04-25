import calendar
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Optional

from config import database
from equity import EquityService
from incomes.errors import IncomesError
from incomes.models import Income, SalaryAnswers
from shared.finances import Currencies, DatabaseCurrencies
from shared.strings import get_number_in_frames
from users import User, UsersService


class IncomesService:
    __DATE_FROAMT = "%Y-%m-%d"
    __MONTHLY_DATE_FROAMT = "%Y-%m"
    __TABLE = "incomes"

    def __init__(self, account_id: int) -> None:
        self._user: Optional[User] = UsersService.fetch_by_account_id(account_id)
        self._date: Optional[date] = None
        self._name: Optional[str] = None
        self._value: Optional[Decimal] = None
        self._currency: Optional[str] = None
        self._salary: Optional[bool] = None

    def set_salary(self, text: str = None) -> None:
        if text is None:
            raise IncomesError("Income type option is not selected")
        if text not in SalaryAnswers.values():
            raise IncomesError("Invalid income option. Please use the keyboard")

        if text == SalaryAnswers.SALARY.value:
            self._salary = True
        elif text == SalaryAnswers.NOT_SALARY.value:
            self._salary = False

    def set_name(self, text: str = None) -> None:
        if text is None:
            raise IncomesError("Category is not selected")

        self._name = text

    def set_currency(self, text: str = None) -> None:
        if text is None:
            raise IncomesError("Value is not added")

        if text not in Currencies.values():
            raise IncomesError("Invalid currency")

        self._currency = Currencies.get_database_value(text)

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
        if not self._name or not self._date or not self._user or not self._value or not self._currency:
            raise IncomesError("One or more mandatory values are not set")

        payload = {
            "name": self._name,
            "value": self._value,
            "currency": self._currency,
            "salary": self._salary,
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

    @classmethod
    def get_detailed_incomes_message(cls, cached_users: dict[int, User], incomes: list[Income]) -> str:
        """Return costs by category in readable format"""
        result = ""

        for income in incomes:
            user: Optional[User] = cached_users.get(income.user_id) or UsersService.fetch_by_id(income.user_id)

            if not user:
                raise IncomesError(f"For some reason there is not user in database related to this income {income}")

            if user.account_id not in cached_users:
                cached_users[user.account_id] = user

            sign = "$" if income.currency == DatabaseCurrencies.USD.value else ""
            fdate = income.date.strftime("%d")

            result += f"{fdate}   {user.full_name} | {income.name} 👉 {income.value} {sign}\n"

        return result

    @classmethod
    def get_formatted_incomes(cls, incomes: list[Income], title="Total incomes") -> str:
        if not incomes:
            return ""

        total_incomes: Decimal = sum(incomes)  # type: ignore

        try:
            sign = "$" if incomes[0].currency == DatabaseCurrencies.USD.value else ""
        except KeyError:
            sign = ""

        return f"<b>{title}</b> 👉 {get_number_in_frames(total_incomes)} {sign}"

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
            raise IncomesError("Invalid monthly date format")

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
            raise IncomesError("Invalid year. Year should be a number")

        start_year = f"{year_num}-01-01"
        end_year = f"{year_num + 1}-01-01"
        q = f"SELECT * from {cls.__TABLE} WHERE date >='{start_year}' and date < '{end_year}' ORDER BY date ASC"
        data = database.raw_execute(q)
        incomes = [Income(**item) for item in data]

        return {currency: list(incomes_iter) for currency, incomes_iter in cls.get_incomes_by_currency(incomes)}
