from typing import Iterable

from shared.domain import Enum


class Currencies(Enum):
    UAH = "🇺🇦 UAH 🇺🇦"
    USD = "🇺🇸 USD 🇺🇸"

    @classmethod
    def get_database_values(cls: Iterable) -> list[str]:
        return [i.name.lower() for i in cls]

    @classmethod
    def get_database_value(cls, value: str) -> str:
        if value == cls.UAH.value:
            return cls.UAH.value.lower()
        if value == cls.USD.value:
            return cls.USD.value.lower()

        raise ValueError("Invalid currency")
