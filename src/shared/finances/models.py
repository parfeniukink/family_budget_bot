from shared.collections import Enum


class DatabaseCurrencies(Enum):
    UAH = "uah"
    USD = "usd"


class Currencies(Enum):
    UAH = "UAH 🇺🇦"
    USD = "$ USD $"

    @classmethod
    def get_database_value(cls, value: str) -> str:
        if value == cls.UAH.value:
            return DatabaseCurrencies.UAH.value
        if value == cls.USD.value:
            return DatabaseCurrencies.USD.value

        raise ValueError("Invalid currency")
