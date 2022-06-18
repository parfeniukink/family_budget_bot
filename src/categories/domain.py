from shared.domain import BaseError, Enum, Model


class CategoriesError(BaseError):
    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        message = message or "No such category"
        super().__init__(message, *args, **kwargs)


class Category(Model):
    id: int
    name: str


class CategoriesMapping(str, Enum):
    FOOD = "🍽 Food"
    RESTAURANTS = "🥗 Restaurants"
    FOOD_DELIVERY = "🍔 Food delivery"
    Roads = "🚌 Roads"
    CLOTHES = "👚 Clothes"
    CAR = "🚙 Car"
    FUEL = "⛽️ Fuel"
    HOUSEHOLD = "🪴 Household"
    HEALTH = "♥️ Health"
    RENTS = "🤝 Rents"
    SERVICES = "💳 Services"
    LEISURE = "🏝 Leisure"
    TECHNICAL_STUFF = "💻 Technical stuff"
    EDUCATION = "📚 Education"
    GIFTS = "🎁 Gifts"
    OTHER = "📦 Other"
    BUSINESS = "💼 Business"
    CURRENCY_TRANSACTIONS = "🔄 Currency transactions"
