from typing import Iterable

from shared.domain import Enum


class Operations(Enum):
    SUBTRACT = "-"
    ADD = "+"


class Currencies(Enum):
    UAH = "🇺🇦 UAH 🇺🇦"
    USD = "🇺🇸 USD 🇺🇸"

    @classmethod
    def get_database_values(cls: Iterable) -> list[str]:
        return [i.name.lower() for i in cls]

    @classmethod
    def get_database_value(cls, value: str) -> str:
        if cls.UAH.name in value.upper():
            return cls.UAH.name.lower()
        if cls.USD.name in value.upper():
            return cls.USD.name.lower()

        raise ValueError("Invalid currency")

    @classmethod
    def get_repr(cls, value: str) -> str:
        if cls.UAH.name in value.upper():
            return cls.UAH.value
        if cls.USD.name in value.upper():
            return cls.USD.value

        raise ValueError("Invalid currency")
