from typing import Optional

from shared.domain import BaseError, Enum, Model


class ConfigurationsGeneralMenu(Enum):
    CONFIGURATIONS = "Configurations ⚙️"


class ConfigurationError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Configuration error"
        super().__init__(message, *args, **kwargs)


class ConfigurationsMenu(Enum):
    GET_ALL = "📜 Get all configurations"
    UPDATE = "📝 Update"


class Configurations(Enum):
    DEFAULT_CURRENCY = "💶 Default currency"
    INCOME_SOURCES = "📄 Patterns for money income sources"
    KEYBOARD_DATES_AMOUNT = "🔢 The amount of dates in keyboard"

    @classmethod
    def get_instance_by_value(cls, val: str) -> Optional[Enum]:
        for el in cls:
            if el.value == val:
                return el


class Configuration(Model):
    id: int
    key: str
    value: str
