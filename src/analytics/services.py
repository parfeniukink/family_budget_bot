from contextlib import suppress
from decimal import Decimal
from itertools import groupby
from operator import attrgetter
from typing import Iterable

from costs import Cost
from costs.models import Category
from costs.services import CategoriesService, CostsService
from incomes.models import Income
from incomes.services import IncomesService
from shared.finances.models import Currencies, DatabaseCurrencies
from shared.sequences import build_dict_from_sequence
from shared.strings import get_number_in_frames
from users import User


class AnalitycsService:
    @classmethod
    def __costs_by_category(cls, costs: list[Cost]):
        attr = "category_id"
        return groupby(sorted(costs, key=attrgetter(attr)), key=attrgetter(attr))

    @classmethod
    def __get_formatted_costs_by_currency_basic(cls, categories_by_id: dict[int, Category], costs: list[Cost]) -> str:
        text = ""
        total_costs_sum: Decimal = sum(costs)  # type: ignore

        for id, costs_group in cls.__costs_by_category(costs):
            category: Category = categories_by_id[id]
            total_costs: Decimal = sum(costs_group)  # type: ignore
            text += "\n" + " 👉 ".join([f"{category.name}", get_number_in_frames(total_costs)])

            percent = (total_costs * Decimal("100") / total_costs_sum).quantize(Decimal("0.1"))
            text += f"    <i>({percent})%</i>"

        text += "\n".join(
            [
                "",
                "",
                f"<b>Total costs</b> 👉 {get_number_in_frames(total_costs_sum)}",
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
                    [f"<b>{category.name}</b>", costs_formatted, "\n"],
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
    def __get_basic_report(
        cls, categories_by_id: dict[int, Category], costs: dict[str, list[Cost]], incomes: dict[str, list[Income]]
    ) -> str:
        uah_costs_message = ""
        usd_costs_message = ""
        uah_salary_incomes_message = ""
        usd_salary_incomes_message = ""
        uah_other_incomes_message = ""
        usd_other_incomes_message = ""

        uah_title = f"\n\n<b><i>{Currencies.UAH.value}</i></b>"
        usd_title = f"\n\n<b><i>{Currencies.USD.value}</i></b>"

        message = "<b>Analytics 📈\n</b>"

        with suppress(KeyError):
            uah_costs_message = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.UAH.value]
            )
        with suppress(KeyError):
            usd_costs_message = cls.__get_formatted_costs_by_currency_basic(
                categories_by_id, costs[DatabaseCurrencies.USD.value]
            )
        with suppress(KeyError):
            uah_salary_incomes_message = IncomesService.get_formatted_incomes(
                [i for i in incomes[DatabaseCurrencies.UAH.value] if i.salary], "Salary"
            )
        with suppress(KeyError):
            usd_salary_incomes_message = IncomesService.get_formatted_incomes(
                [i for i in incomes[DatabaseCurrencies.USD.value] if i.salary], "Salary"
            )
        with suppress(KeyError):
            uah_other_incomes_message = IncomesService.get_formatted_incomes(
                [i for i in incomes[DatabaseCurrencies.UAH.value] if not i.salary], "Other incomes"
            )
        with suppress(KeyError):
            usd_other_incomes_message = IncomesService.get_formatted_incomes(
                [i for i in incomes[DatabaseCurrencies.USD.value] if not i.salary], "Other incomes"
            )

        if uah_costs_message or uah_salary_incomes_message:
            message += "\n".join([uah_title, uah_costs_message, uah_salary_incomes_message, uah_other_incomes_message])

        if usd_costs_message or usd_salary_incomes_message:
            message += "\n".join([usd_title, usd_costs_message, usd_salary_incomes_message, usd_other_incomes_message])

        return message

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
        uah_incomes: str = IncomesService.get_detailed_incomes_message(
            cached_users, incomes[DatabaseCurrencies.UAH.value]
        )
        usd_incomes: str = IncomesService.get_detailed_incomes_message(
            cached_users, incomes[DatabaseCurrencies.USD.value]
        )

        incomes_message = "\n".join(["<b>Incomes 💸\n</b>", uah_incomes, usd_incomes])
        report.append(incomes_message)

        return report

    @classmethod
    def get_monthly_basic_report(cls, month: str) -> Iterable[str]:
        costs: dict[str, list[Cost]] = CostsService.get_monthly_costs(month)
        incomes: dict[str, list[Income]] = IncomesService.get_monthly_incomes(month)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        report = cls.__get_basic_report(categories_by_id, costs, incomes)

        return [report]

    @classmethod
    def get_annyally_report(cls, year: str) -> str:
        """Get annually report. Costs by category. All incomes"""
        costs: dict[str, list[Cost]] = CostsService.get_annually_costs(year)
        incomes: dict[str, list[Income]] = IncomesService.get_annually_incomes(year)
        categories_by_id: dict[int, Category] = build_dict_from_sequence(
            CategoriesService.CACHED_CATEGORIES,
            "id",
        )  # type: ignore

        report = cls.__get_basic_report(categories_by_id, costs, incomes)

        return report
