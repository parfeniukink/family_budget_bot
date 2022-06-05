from typing import Optional

from shared.domain import BaseError, Enum, Model


class CategoriesError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "No such category"
        super().__init__(message, *args, **kwargs)


class Category(Model):
    id: int
    name: str


class CategoriesMapping(str, Enum):
    FOOD = "🍽 Foo"
    RESTAURANTS = "🥗 Restaurants"
    FOOD_DELIVERY = "🍔 Food delivery"
    Roads = "🚌 Roads"
    CLOTHES = "👚 Clothes"
    CAR = "🚙 Car"
    FUEL = "⛽️ Fuel"
    HOUSEHOLD = "🪴 Household"
    RENTS = "🤝 Rents"
    SERVICES = "💳 Services"
    LEISURE = "🏝 Leisur"
    TECHNICAL_STUFF = "💻 Technical stuff"
    EDUCATION = "📚 Education"
    GIFTS = "🎁 Gifts"
    OTHER = "📦 Other"
    CURRENCY_TRANSACTIONS = "🔄 Currency transactions"
