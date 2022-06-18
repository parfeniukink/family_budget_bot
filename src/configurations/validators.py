from typing import Callable

from configurations.domain import (
    ConfigurationError,
    Configurations,
    ConfigurationsStorage,
)


def validate_new_dates_keyboard_len(value: str) -> None:
    try:
        converted_value = int(value)
    except ValueError:
        raise ConfigurationError("Value should a valid integer")
    if converted_value < 1:
        raise ConfigurationError("Value should be greater than 0")
    elif converted_value > 31:
        raise ConfigurationError("Value should be less than 31")


def configurations_validator_dispatcher(storage: ConfigurationsStorage) -> Callable[[str], None]:
    if storage.configuration_name == Configurations.KEYBOARD_DATES_AMOUNT.name.lower():
        return validate_new_dates_keyboard_len

    return lambda _: None
