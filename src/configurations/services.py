from typing import Optional

import messages
from configurations.domain import Configuration, ConfigurationError, Configurations
from db import database
from finances import Currencies
from shared.domain import Enum


class ConfigurationsCache(type):
    __TABLE = "configurations"

    @classmethod
    def get_configurations(cls) -> list[Configuration]:
        return [Configuration(**item) for item in database.fetchall(cls.__TABLE)]

    def __getattr__(cls, attr):
        if attr == "CACHED_CONFIGURATIONS":
            data = cls.get_configurations()
            setattr(cls, attr, data)
            return data
        raise AttributeError(attr)


class ConfigurationsService(metaclass=ConfigurationsCache):
    __TABLE = "configurations"
    CACHED_CONFIGURATIONS: list[Configuration]

    @classmethod
    def get_by_name(cls, name: str) -> Configuration:
        for configuration in cls.CACHED_CONFIGURATIONS:
            if configuration.key == name:
                return configuration
        raise ConfigurationError(f"No such confuguration {name}")

    @classmethod
    def get_all_formatted(cls) -> str:
        configurations = "\n\n".join(
            [f"{getattr(Configurations, c.key.upper()).value} 👉 {c.value}" for c in cls.CACHED_CONFIGURATIONS],
        )
        return messages.CONFIGURATIONS_LIST.format(configurations=configurations)

    @classmethod
    def data_is_valid(cls, data: tuple[str, Optional[str]]) -> None:
        if len(data) != 2:
            raise ConfigurationError("Invalid configuratoin update payload")
        if not data[1]:
            raise ConfigurationError("Configuration value is not set")
        if data[0] not in Configurations.values():
            raise ConfigurationError("Invalid configuratoin selected")
        if data[0] == Configurations.DEFAULT_CURRENCY.value and data[1] not in Currencies.get_database_values():
            raise ConfigurationError(f"Invalid currency. Allowed: {Currencies.get_database_values()}")
        if data[0] == Configurations.INCOME_SOURCES.value and ", " in data[1]:
            text = "\n".join(
                (
                    "Invalid format. All configurations should match match next pattern:",
                    "<code>value,value,value</code>",
                    "",
                    "Spaces not allowed between values. Use only comma.",
                    "",
                    "Example:",
                    "<b>My new job,Design</b>",
                )
            )
            raise ConfigurationError(text)
        if data[0] == Configurations.KEYBOARD_DATES_AMOUNT.value:
            try:
                int(data[1])
            except ValueError:
                raise ConfigurationError("This value should be an integer")

    @classmethod
    def update(cls, data: tuple[str, Optional[str]]) -> Configuration:
        cls.data_is_valid(data)

        config_name: Optional[Enum] = Configurations.get_instance_by_value(data[0])
        if not config_name:
            raise ConfigurationError(f"Can not find configuration {config_name} in database")

        update_data: dict = database.update(
            cls.__TABLE, data=("value", str(data[1])), condition=("key", config_name.name.lower())
        )
        configuration = Configuration(**update_data)

        for c in cls.CACHED_CONFIGURATIONS:
            if c.id == configuration.id:
                c.value = configuration.value

        return configuration
