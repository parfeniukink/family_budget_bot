from datetime import date, timedelta
from typing import Iterable, Optional

from loguru import logger

from db import database
from shared.domain import BaseError
from shared.sequences import without_duplicates


class DatesCache(type):
    """Use as metaclass"""

    COSTS_TABLE = "costs"

    @classmethod
    def get_dates(cls) -> Optional[tuple[date, date]]:
        first_date = database.raw_execute(f"SELECT date from {cls.COSTS_TABLE} ORDER BY date ASC LIMIT 1")[0]["date"]
        last_date = database.raw_execute(f"SELECT date from {cls.COSTS_TABLE} ORDER BY date DESC LIMIT 1")[0]["date"]
        try:
            return first_date, last_date
        except IndexError:
            return None

    @classmethod
    def set_dates(cls) -> Optional[tuple[date, date]]:
        dates = cls.get_dates()

        if not dates:
            return None

        first_date = dates[0]
        last_date = dates[1]

        setattr(cls, "FIRST_DATE", first_date)
        setattr(cls, "LAST_DATE", last_date)

        logger.info("Update dates cache")

        return dates

    def __getattr__(cls, attr):
        if attr == "FIRST_DATE" or attr == "LAST_DATE":
            dates = cls.set_dates()

            if not dates:
                return None

            if attr == "FIRST_DATE":
                return dates[0]

            if attr == "LAST_DATE":
                return dates[1]

        raise AttributeError(attr)


class DatesService(metaclass=DatesCache):
    @classmethod
    def __get_monthes_in_range(cls, first_date: date, last_date: date, date_format: str = "%Y-%m") -> list[str]:
        results = []
        while last_date > first_date:
            results.append(last_date.strftime(date_format))
            last_date -= timedelta(days=last_date.day)

        return results

    @classmethod
    def get_formatted_dates(cls, date_format: str = "%Y-%m") -> Iterable:
        """Return the list of dates from the first saved cost to today in format YEAR-MONTH"""

        if not cls.FIRST_DATE or not cls.LAST_DATE:
            raise BaseError("Currently we do not have any costs in database")

        if all([cls.FIRST_DATE.year == cls.LAST_DATE.year, cls.FIRST_DATE.month == cls.LAST_DATE.month]):
            return list(cls.FIRST_DATE.strftime(date_format))

        data: list[str] = cls.__get_monthes_in_range(cls.FIRST_DATE, cls.LAST_DATE, date_format)

        if not date.today().strftime(date_format) in data:
            DatesCache.set_dates()
            data: list[str] = cls.__get_monthes_in_range(cls.FIRST_DATE, cls.LAST_DATE, date_format)

        return without_duplicates(reversed(data))
