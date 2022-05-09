import calendar
from datetime import date, datetime
from decimal import Decimal
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Optional

from categories import CategoriesService, Category
from configurations import ConfigurationsService
from costs.domain import Cost, CostsError, CostsStorage
from db import database
from equity import EquityCRUD
from finances.domain import Currencies, Operations
from shared.formatting import get_number_in_frames
from users import User, UsersCRUD


class CostsCRUD:
    __TABLE = "costs"

    @classmethod
    def get_by_id(cls, cost_id: str) -> Optional[Cost]:
        data: Optional[dict] = database.fetch(cls.__TABLE, "id", cost_id)
        return Cost(**data) if data else None

    @classmethod
    def delete_by_id(cls, cost_id: str) -> None:
        database.delete(cls.__TABLE, "id", cost_id)


class CostsService:
    __FULL_DATE_FROAMT = "%Y-%m-%d"
    __MONTHLY_DATE_FROAMT = "%Y-%m"
    __TABLE = "costs"

    def __init__(self, account_id: int) -> None:
        self._user: Optional[User] = UsersCRUD.fetch_by_account_id(account_id)
        self._category: Optional[Category] = None
        self._date: Optional[date] = None
        self._text: Optional[str] = None
        self._value: Optional[Decimal] = None

    @classmethod
    def save_costs(cls, storage: CostsStorage) -> Cost:
        if not all((storage.description, storage.date, storage.category, storage.value)):
            raise CostsError("One or more mandatory values are not set")

        user: User = UsersCRUD.fetch_by_account_id(storage.account_id)
        default_currency: str = ConfigurationsService.get_by_name("default_currency").value

        payload = {
            "name": storage.description,
            "value": storage.value,
            "currency": default_currency,
            "date": storage.date,
            "user_id": user.id,
            "category_id": storage.category.id,  # type: ignore
        }
        data: dict = database.insert(cls.__TABLE, payload)
        cost = Cost(**data)

        EquityCRUD.update(
            operation=Operations.SUBTRACT,
            value=cost.value,
            currency=cost.currency,
        )

        return cost

    @staticmethod
    def get_formatted_cost(cost: Cost) -> str:
        category: Optional[Category] = CategoriesService.get_by_id(cost.category_id)
        user = UsersCRUD.fetch_by_id(cost.user_id)

        if not user:
            raise CostsError("⚠️ For some reason cost {cost.id} doesn't have user")
        if not category:
            raise CostsError("⚠️ For some reason cost {cost.id} doesn't have category")

        currency_sign = "$" if cost.currency == Currencies.get_database_value("USD") else ""
        cost_date = cost.date.strftime("%d-%m")

        return (
            f"{cost.id}  {cost.name} 👉 {get_number_in_frames(cost.value)}{currency_sign}   <i>({cost_date})</i>  "
            f"by {user.full_name} "
        )

    @classmethod
    def get_formatted_costs_for_delete(cls, costs: list[Cost]) -> str:
        return "\n".join(cls.get_formatted_cost(cost) for cost in costs)

    @staticmethod
    def get_costs_by_currency(costs: list[Cost]) -> Iterable:
        attr = "currency"
        return groupby(sorted(costs, key=attrgetter(attr)), key=attrgetter(attr))

    @classmethod
    def get_monthly_costs(cls, date: str, category: Optional[Category] = None) -> dict[str, list[Cost]]:
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

        category_filter_query = f"and category_id={int(category.id)}" if category else ""
        q = (
            f"SELECT * from {cls.__TABLE} WHERE date >='{start_date}' "
            f"and date <= '{end_date}' "
            f"{category_filter_query} ORDER BY date ASC"
        )

        data = database.raw_execute(q)
        costs = [Cost(**item) for item in data]

        return {currency: list(costs_iter) for currency, costs_iter in cls.get_costs_by_currency(costs)}

    @classmethod
    def get_annually_costs(cls, year: str) -> dict[str, list[Cost]]:
        """
        Return the list of costs for the specific year by currency.
        Used mostly for analytics.
        """
        try:
            year_num = int(year)
        except ValueError:
            raise CostsError("Invalid year. Year should be a number")

        start_year = f"{year_num}-01-01"
        end_year = f"{year_num + 1}-01-01"
        q = f"SELECT * from {cls.__TABLE} WHERE date >='{start_year}' and date < '{end_year}' ORDER BY date ASC"
        data = database.raw_execute(q)
        costs = [Cost(**item) for item in data]

        return {currency: list(costs_iter) for currency, costs_iter in cls.get_costs_by_currency(costs)}

    @classmethod
    def get_by_id(cls, cost_id: str) -> None:
        database.delete(cls.__TABLE, "id", cost_id)

    @classmethod
    def delete_by_id(cls, cost_id: str) -> None:
        database.delete(cls.__TABLE, "id", cost_id)
