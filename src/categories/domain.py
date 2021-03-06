from shared.domain import BaseError, Enum, Model


class CategoriesError(BaseError):
    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        message = message or "No such category"
        super().__init__(message, *args, **kwargs)


class Category(Model):
    id: int
    name: str


class CategoriesMapping(str, Enum):
    BUSINESS = "ðž Business"
    DEBTS = "ðļ Debts"
    CURRENCY_TRANSACTIONS = "ð Currency transactions"
    Roads = "ð Roads"
    CLOTHES = "ð Clothes"
    LEISURE = "ð Leisure"
    RENTS = "ðĪ Rents"
    SERVICES = "ðģ Services"
    TECHNICAL_STUFF = "ðŧ Technical stuff"
    EDUCATION = "ð Education"
    GIFTS = "ð Gifts"
    CAR = "ð Car"
    FUEL = "â―ïļ Fuel"
    HOUSEHOLD = "ðŠī Household"
    HEALTH = "âĨïļ Health"
    OTHER = "ðĶ Other"
    FOOD_DELIVERY = "ð Food delivery"
    RESTAURANTS = "ðĨ Restaurants"
    FOOD = "ð― Food"
