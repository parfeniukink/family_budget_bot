from typing import Optional

from shared.collections import Enum


class Configurations(Enum):
    DEFAULT_CURRENCY = "💶 Default currency"
    INCOME_SOURCES = "📄 Patterns for money income sources"
    KEYBOARD_DATES_AMOUNT = "🔢 The amount of dates in keyboard"

    @classmethod
    def get_instance_by_value(cls, val: str) -> Optional[Enum]:
        for el in cls:
            if el.value == val:
                return el


class DefaultCurrencies(Enum):
    USD = "usd"
    UAH = "uah"
