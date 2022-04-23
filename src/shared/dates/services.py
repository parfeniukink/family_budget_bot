from datetime import date, timedelta
from typing import Iterable, Optional

from config import database
from shared.errors import UserError
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


class DatesService(metaclass=DatesCache):
    @classmethod
    def get_formatted_dates(cls, date_format: str = "%Y-%m") -> Iterable:
        """Return the list of dates from the first saved cost to today in format YEAR-MONTH"""
        if not cls.FIRST_DATE or not cls.LAST_DATE:
            raise UserError("Currently we do not have any costs in database")

        if all([cls.FIRST_DATE.year == cls.LAST_DATE.year, cls.FIRST_DATE.month == cls.LAST_DATE.month]):
            return list(cls.FIRST_DATE.strftime(date_format))

        data = [
            (cls.FIRST_DATE + timedelta(_)).strftime(date_format)
            for _ in range(
                (cls.LAST_DATE - cls.FIRST_DATE).days,
            )
        ]

        return without_duplicates(reversed(data))
