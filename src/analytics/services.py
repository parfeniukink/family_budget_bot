from contextlib import suppress
from datetime import date, timedelta
from decimal import Decimal
from itertools import groupby
from operator import attrgetter
from typing import Optional
from analytics.errors import AnalyticsError

from config import database
from costs import Cost
from costs.models import Category
from costs.services import CategoriesService, CostsService
from shared.finances.models import Currencies, DatabaseCurrencies
from shared.sequences import build_dict_from_sequence


class AnalyticsCache(type):
    COSTS_TABLE = "costs"

    @classmethod
    def get_first_date(cls) -> Optional[date]:
        data = database.raw_execute(f"SELECT date from {cls.COSTS_TABLE} ORDER BY date ASC LIMIT 1")
        try:
            return data[0]["date"]
        except IndexError:
            return None

    def __getattr__(cls, attr):
        if attr == "FIRST_DATE":
            data = cls.get_first_date()
            setattr(cls, attr, data)
            return data
        raise AttributeError(attr)


class AnalitycsService(metaclass=AnalyticsCache):
    FIRST_DATE: Optional[date]
    DATE_FORMAT = "%Y-%m"

    @classmethod
    def get_formatted_dates(cls) -> set[str]:
        """Return the list of dates from the first saved cost to today in format YEAR-MONTH"""
        if not cls.FIRST_DATE:
            raise AnalyticsError("Currently we do not have any costs in database")

        end: date = date.today()
        data = {(cls.FIRST_DATE + timedelta(_)).strftime(cls.DATE_FORMAT) for _ in range((end - cls.FIRST_DATE).days)}

        return data

    @classmethod
    def __costs_by_category(cls, costs: list[Cost]):
        attr = "category_id"
        return groupby(sorted(costs, key=attrgetter(attr)), key=attrgetter(attr))

    @classmethod
    def __get_formatted_costs_by_currency_basic(cls, categories_by_id: dict[int, Category], costs: list[Cost]) -> str:
        text = ""
        total_sum: Decimal = sum(costs)  # type: ignore

        for id, costs_group in cls.__costs_by_category(costs):
            category: Category = categories_by_id[id]
            total_costs: Decimal = sum(costs_group)  # type: ignore
            text += "\n\n" + ":  ".join([f"{category.name}", str(total_costs)])

            percent = (total_costs * Decimal("100") / total_sum).quantize(Decimal("0.1"))
            text += f"    <i>({percent})%</i>"

        text += f"\n\nTotal costs: {str(total_sum)}"

        return text

    @classmethod
    def __get_formatted_costs_by_currency_detailed(
        cls, categories_by_id: dict[int, Category], costs: list[Cost]
    ) -> str:
        text = ""

        for id, costs_group in cls.__costs_by_category(costs):
            category: Category = categories_by_id[id]
            costs_formatted: str = "\n".join([f"    <i>{cost.name} -- {cost.value}</i>" for cost in costs_group])
            text += "\n".join([f"<b>{category.name}</b>", costs_formatted, "\n"])

        return text

    @classmethod
    def get_monthly_basic_report(cls, month: str) -> str:
        costs: dict[str, list[Cost]] = CostsService.get_monthly_costs(month)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        message = "<b>Analytics 📈\n</b>"

        with suppress(KeyError):
            uah_costs = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.UAH.value]
            )
            _uah_title = f"\n\n<b><i>{Currencies.UAH.value}</i></b>"
            message += "".join((_uah_title, uah_costs))

        with suppress(KeyError):
            usd_costs = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.USD.value]
            )

            if usd_costs:
                _uah_title = f"\n\n<b><i>{Currencies.USD.value}</i></b>"
                message += "".join((_uah_title, usd_costs))

        return message

    @classmethod
    def get_monthly_detailed_report(cls, month: str) -> str:
        costs: dict[str, list[Cost]] = CostsService.get_monthly_costs(month)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        message = "<b>Analytics 📈\n</b>"

        with suppress(KeyError):
            uah_costs = cls.__get_formatted_costs_by_currency_detailed(
                categories_by_id, costs[DatabaseCurrencies.UAH.value]
            )

            if uah_costs:
                _uah_title = f"\n\n<b><i>{Currencies.UAH.value}</i></b>\n\n"
                message += "".join((_uah_title, uah_costs))

        with suppress(KeyError):
            usd_costs = cls.__get_formatted_costs_by_currency_detailed(
                categories_by_id, costs[DatabaseCurrencies.USD.value]
            )

            if usd_costs:
                _uah_title = f"\n\n<b><i>{Currencies.USD.value}</i></b>\n\n"
                message += "".join((_uah_title, usd_costs))

        return message
