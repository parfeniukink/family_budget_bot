from typing import Callable

from configurations.domain import (
    ConfigurationError,
    Configurations,
    ConfigurationsStorage,
)
from shared.messages import BOLD, CODE


def validate_new_dates_keyboard_len(value: str) -> None:
    try:
        converted_value = int(value)
    except ValueError:
        raise ConfigurationError("Value should a valid integer")
    if converted_value < 1:
        raise ConfigurationError("Value should be greater than 0")


def validate_new_income_sources(value: str) -> None:
    message = "\n".join(
        (
            "Invalid format. All configurations should match match next pattern:",
            CODE.format(text="value,value,value"),
            "",
            "Spaces not allowed between values. Use only comma.",
            "",
            "Example:",
            BOLD.format(text="My new job,Design"),
        )
    )
    if ", " in value:
        raise ConfigurationError(message)


def configurations_validator_dispatcher(storage: ConfigurationsStorage) -> Callable[[str], None]:
    if storage.configuration_name == Configurations.KEYBOARD_DATES_AMOUNT.name.lower():
        return validate_new_dates_keyboard_len
    elif storage.configuration_name == Configurations.INCOME_SOURCES.name.lower():
        return validate_new_income_sources

    return lambda _: None
