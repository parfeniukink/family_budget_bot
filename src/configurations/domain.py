from shared.domain import BaseError, CallbackItem, Enum, Model, random_uuid
from storages import Storage


class ConfigurationsGeneralMenu(Enum):
    CONFIGURATIONS = "Configurations ⚙️"


class ConfigurationError(BaseError):
    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        message = message or "Configuration error"
        super().__init__(message, *args, **kwargs)


class ConfigurationsMenu(Enum):
    GET_ALL = CallbackItem(name="📜 Get all configurations")
    EDIT = CallbackItem(name="📝 Edit")


class Configurations(Enum):
    DEFAULT_CURRENCY = "Default currency"
    INCOME_SOURCES = "Money incomes sources"
    KEYBOARD_DATES_AMOUNT = "The amount of dates in keyboard"

    @classmethod
    def get_instance_by_value(cls, val: str) -> Enum | None:
        for el in cls:
            if el.value == val:
                return el
        return None


class Configuration(Model):
    id: int
    default_currency: str
    income_sources: str | None
    keyboard_dates_amount: int
    user_id: int


class ExtraCallbackData(Enum):
    CONFIGURATION_SELECTED = random_uuid()
    CONFIRMATION_SELECTED = random_uuid()
    CURRENCY_SELECTED = random_uuid()


class ConfigurationsStorage(Storage):
    __slots__ = "configuration_name", "value"

    def __init__(self, account_id: int) -> None:
        if getattr(self, "__initialized", False):
            return

        super().__init__(account_id)
        self.configuration_name: str | None = None
        self.value: str | None = None
