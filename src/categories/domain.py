from shared.domain import BaseError, Enum, Model


class CategoriesError(BaseError):
    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        message = message or "No such category"
        super().__init__(message, *args, **kwargs)


class Category(Model):
    id: int
    name: str


class CategoriesMapping(str, Enum):
    BUSINESS = "💼 Business"
    DEBTS = "💸 Debts"
    CURRENCY_TRANSACTIONS = "🔄 Currency transactions"
    Roads = "🚌 Roads"
    CLOTHES = "👚 Clothes"
    LEISURE = "🏝 Leisure"
    RENTS = "🤝 Rents"
    SERVICES = "💳 Services"
    TECHNICAL_STUFF = "💻 Technical stuff"
    EDUCATION = "📚 Education"
    GIFTS = "🎁 Gifts"
    CAR = "🚙 Car"
    FUEL = "⛽️ Fuel"
    HOUSEHOLD = "🪴 Household"
    HEALTH = "♥️ Health"
    OTHER = "📦 Other"
    FOOD_DELIVERY = "🍔 Food delivery"
    RESTAURANTS = "🥗 Restaurants"
    FOOD = "🍽 Food"
