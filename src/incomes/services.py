import calendar
from datetime import datetime
from decimal import Decimal
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Optional

from db import database
from equity import EquityCRUD
from finances import Currencies, Operations
from incomes.domain import Income, IncomesError, IncomesStorage
from incomes.messages import (
    INCOME_DETAILED_ITEM_MESSAGE,
    INCOME_GET_NO_USER_ERROR,
    MONTHLY_DATE_FORMAT_INVALID,
    TOTAL_INCOMES_LIST_MESSAGE,
    YEAR_FORMAT_INVALID,
)
from shared.formatting import get_number_in_frames
from users import User, UsersCRUD


class IncomesCRUD:
    __TABLE = "incomes"

    @classmethod
    def save(cls, storage: IncomesStorage):
        user: User = UsersCRUD.fetch_by_account_id(storage.account_id)

        payload = {
            "name": storage.description,
            "value": storage.value,
            "currency": storage.currency,
            "salary": storage.salary,
            "date": storage.date,
            "user_id": user.id,
        }
        data: dict = database.insert(cls.__TABLE, payload)
        income = Income(**data)

        EquityCRUD.update(
            operation=Operations.ADD,
            value=income.value,
            currency=income.currency,
        )

        return income


class IncomesService:
    __MONTHLY_DATE_FROAMT = "%Y-%m"
    __TABLE = "incomes"

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
                fdate=fdate,
                user=user.full_name,
                income_name=income.name,
                income_value=get_number_in_frames(income.value),
                sign=sign,
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
