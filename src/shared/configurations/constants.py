from shared.collections import Enum


class Configurations(Enum):
    DEFAULT_CURRENCY = "default_currency"
    INCOME_SOURCES = "income_sources"


class DefaultCurrencies(Enum):
    USD = "usd"
    UAH = "uah"
