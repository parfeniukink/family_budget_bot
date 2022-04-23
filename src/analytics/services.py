from contextlib import suppress
from datetime import date, timedelta
from decimal import Decimal
from itertools import groupby
from operator import attrgetter
from typing import Iterable, Optional

from analytics.errors import AnalyticsError
from config import database
from costs import Cost
from costs.models import Category
from costs.services import CategoriesService, CostsService
from incomes.models import Income
from incomes.services import IncomesService
from shared.categories import CATEGORIES_EMOJI
from shared.finances.models import Currencies, DatabaseCurrencies
from shared.sequences import build_dict_from_sequence, without_duplicates
from shared.strings import get_number_in_frames
from users import User, UsersService


class AnalyticsCache(type):
    COSTS_TABLE = "costs"

    @classmethod
    def get_dates(cls) -> Optional[tuple[date, date]]:
        first_date = database.raw_execute(f"SELECT date from {cls.COSTS_TABLE} ORDER BY date ASC LIMIT 1")[0]["date"]
        last_date = database.raw_execute(f"SELECT date from {cls.COSTS_TABLE} ORDER BY date DESC LIMIT 1")[0]["date"]
        try:
            return first_date, last_date
        except IndexError:
            return None

    def __getattr__(cls, attr):
        if attr == "FIRST_DATE" or attr == "LAST_DATE":
            dates = cls.get_dates()

            if not dates:
                return None

            first_date = dates[0]
            last_date = dates[1]

            setattr(cls, "FIRST_DATE", first_date)
            setattr(cls, "LAST_DATE", last_date)

            if attr == "FIRST_DATE":
                return first_date

            if attr == "LAST_DATE":
                return last_date

        raise AttributeError(attr)


class AnalitycsService(metaclass=AnalyticsCache):
    FIRST_DATE: Optional[date]
    DATE_FORMAT = "%Y-%m"

    @classmethod
    def get_formatted_dates(cls, date_format: str = "%Y-%m") -> Iterable:
        """Return the list of dates from the first saved cost to today in format YEAR-MONTH"""
        if not cls.FIRST_DATE or not cls.LAST_DATE:
            raise AnalyticsError("Currently we do not have any costs in database")

        if all([cls.FIRST_DATE.year == cls.LAST_DATE.year, cls.FIRST_DATE.month == cls.LAST_DATE.month]):
            return list(cls.FIRST_DATE.strftime(date_format))

        data = [
            (cls.FIRST_DATE + timedelta(_)).strftime(date_format)
            for _ in range(
                (cls.LAST_DATE - cls.FIRST_DATE).days,
            )
        ]

        return without_duplicates(reversed(data))

    @classmethod
    def __costs_by_category(cls, costs: list[Cost]):
        attr = "category_id"
        return groupby(sorted(costs, key=attrgetter(attr)), key=attrgetter(attr))

    @classmethod
    def __get_formatted_costs_by_currency_basic(
        cls, categories_by_id: dict[int, Category], costs: list[Cost], incomes: dict[str, list[Income]]
    ) -> str:
        text = ""
        total_costs_sum: Decimal = sum(costs)  # type: ignore
        total_uah_incomes: Decimal = sum(incomes[DatabaseCurrencies.UAH.value])  # type: ignore
        total_usd_incomes: Decimal = sum(incomes[DatabaseCurrencies.USD.value])  # type: ignore

        for id, costs_group in cls.__costs_by_category(costs):
            category: Category = categories_by_id[id]
            total_costs: Decimal = sum(costs_group)  # type: ignore
            text += "\n" + " 👉 ".join(
                [f"{CATEGORIES_EMOJI.get(category.name, '')} {category.name}", get_number_in_frames(total_costs)]
            )

            percent = (total_costs * Decimal("100") / total_costs_sum).quantize(Decimal("0.1"))
            text += f"    <i>({percent})%</i>"

        text += "\n".join(
            [
                "",
                "",
                "⬇️ ⬇️ ⬇️ ⬇️ ⬇️",
                f"Total costs 👉 {get_number_in_frames(total_costs_sum)}",
                f"Total UAH incomes 👉 {get_number_in_frames(total_uah_incomes)}",
                f"Total USD incomes 👉 {get_number_in_frames(total_usd_incomes)} $",
            ]
        )

        return text

    @classmethod
    def __get_formatted_costs_by_currency_detailed(
        cls, categories_by_id: dict[int, Category], costs: list[Cost]
    ) -> list[str]:
        report: list[str] = []

        for id, costs_group in cls.__costs_by_category(costs):
            category: Category = categories_by_id[id]
            costs_formatted = ""

            for cost in costs_group:
                cost_date = cost.date.strftime("%d")
                costs_formatted += f"\n    {cost_date}  {cost.name} 👉 {get_number_in_frames(cost.value)}"

            report.append(
                "\n".join(
                    [f"<b>{CATEGORIES_EMOJI.get(category.name, '')} {category.name}</b>", costs_formatted, "\n"],
                )
            )

        return report

    @classmethod
    def __get_detailed_costs(cls, categories_by_id: dict[int, Category], costs: list[Cost], header: str) -> list[str]:
        """Return costs by category in readable format"""
        results: list[str] = []
        rcosts = [el for el in cls.__get_formatted_costs_by_currency_detailed(categories_by_id, costs)]

        if rcosts:
            results.append(f"<b><i>{header}</i></b>")
            results += rcosts

        return results

    @classmethod
    def __get_detailed_incomes_message(cls, cached_users: dict[int, User], incomes: list[Income]) -> str:
        """Return costs by category in readable format"""
        result = ""

        for income in incomes:
            user: Optional[User] = cached_users.get(income.user_id) or UsersService.fetch_by_id(income.user_id)

            if not user:
                raise AnalyticsError(f"For some reason there is not user in database related to this income {income}")

            if user.account_id not in cached_users:
                cached_users[user.account_id] = user

            sign = "$" if income.currency == DatabaseCurrencies.USD.value else ""
            fdate = income.date.strftime("%d")

            result += f"{fdate}   {user.full_name} | {income.name} 👉 {income.value} {sign}\n"

        return result

    @classmethod
    def get_monthly_basic_report(cls, month: str) -> Iterable[str]:
        costs: dict[str, list[Cost]] = CostsService.get_monthly_costs(month)
        incomes: dict[str, list[Income]] = IncomesService.get_monthly_incomes(month)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        message = "<b>Analytics 📈\n</b>"

        with suppress(KeyError):
            uah_costs = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.UAH.value], incomes
            )
            _uah_title = f"\n\n<b><i>{Currencies.UAH.value}</i></b>"
            message += "".join((_uah_title, uah_costs))

        with suppress(KeyError):
            usd_costs = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.USD.value], incomes
            )

            if usd_costs:
                _uah_title = f"\n\n<b><i>{Currencies.USD.value}</i></b>"
                message += "".join((_uah_title, usd_costs))

        return [message]

    @classmethod
    def get_monthly_detailed_report(cls, month: str) -> Iterable[str]:
        """
        This is a general interface to get monthly costs and incomes analytics
        Return the list of costs by category with headers.
        The last element in the list is incomes
        """
        costs: dict[str, list[Cost]] = CostsService.get_monthly_costs(month)
        incomes: dict[str, list[Income]] = IncomesService.get_monthly_incomes(month)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        report = []
        report.append("<b>Analytics 📈</b>")
        with suppress(KeyError):
            report.extend(
                cls.__get_detailed_costs(categories_by_id, costs[DatabaseCurrencies.UAH.value], Currencies.UAH.value)
            )
        with suppress(KeyError):
            report.extend(
                cls.__get_detailed_costs(categories_by_id, costs[DatabaseCurrencies.USD.value], Currencies.USD.value)
            )

        cached_users: dict[int, User] = {}
        uah_incomes: str = cls.__get_detailed_incomes_message(cached_users, incomes[DatabaseCurrencies.UAH.value])
        usd_incomes: str = cls.__get_detailed_incomes_message(cached_users, incomes[DatabaseCurrencies.USD.value])
        incomes_message = "\n".join(["<b>Incomes 💸\n</b>", uah_incomes, usd_incomes])
        report.append(incomes_message)

        return report

    @classmethod
    def get_annyally_report(cls, year: str) -> str:
        """Get annually report. Costs by category. All incomes"""
        costs: dict[str, list[Cost]] = CostsService.get_annually_costs(year)
        incomes: dict[str, list[Income]] = IncomesService.get_annually_incomes(year)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        message = "<b>Analytics 📈\n</b>"

        with suppress(KeyError):
            uah_costs = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.UAH.value], incomes
            )
            _uah_title = f"\n\n<b><i>{Currencies.UAH.value}</i></b>"
            message += "".join((_uah_title, uah_costs))

        with suppress(KeyError):
            usd_costs = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.USD.value], incomes
            )

            if usd_costs:
                _uah_title = f"\n\n<b><i>{Currencies.USD.value}</i></b>"
                message += "".join((_uah_title, usd_costs))

        return message
