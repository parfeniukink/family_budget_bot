from typing import Optional

from configurations.domain import Configuration, ConfigurationError, Configurations
from configurations.messages import (
    CONFIGURATION_INCOME_SOURCE_PAYLOAD_ERROR,
    CONFIGURATION_INVALID_MESSAGE,
    CONFIGURATION_UPDATE_PAYLOAD_INVALID_MESSAGE,
    CONFIGURATION_VALUE_IS_NOT_SET_MESSAGE,
    CONFIGURATION_VALUE_VALUE_ERROR,
    CONFIGURATION_WAS_NOT_FOUND_MESSAGE,
)
from db import database
from finances import Currencies
from shared import messages
from shared.domain import Enum
from shared.messages import BOLD, LINE_ITEM

__all__ = ("ConfigurationsService",)


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
        raise ConfigurationError(CONFIGURATION_WAS_NOT_FOUND_MESSAGE.format(config_name=name))

    @classmethod
    def get_all_formatted(cls) -> str:
        configurations = "\n\n".join(
            (
                [
                    LINE_ITEM.format(key=getattr(Configurations, c.key.upper()).value, value=c.value)
                    for c in cls.CACHED_CONFIGURATIONS
                ]
            )
        )
        return "\n\n\n".join((BOLD.format(text="⚙️ Active configuratoins"), configurations))

    @classmethod
    def data_is_valid(cls, data: tuple[str, Optional[str]]) -> None:
        if len(data) != 2:
            raise ConfigurationError(CONFIGURATION_UPDATE_PAYLOAD_INVALID_MESSAGE)
        if not data[1]:
            raise ConfigurationError(CONFIGURATION_VALUE_IS_NOT_SET_MESSAGE)
        if data[0] not in Configurations.values():
            raise ConfigurationError(CONFIGURATION_INVALID_MESSAGE)
        if data[0] == Configurations.DEFAULT_CURRENCY.value and data[1] not in Currencies.get_database_values():
            raise ConfigurationError(messages.CURRENCY_INVALID_ERROR.format(allowed=Currencies.get_database_values()))
        if data[0] == Configurations.INCOME_SOURCES.value and ", " in data[1]:
            raise ConfigurationError(CONFIGURATION_INCOME_SOURCE_PAYLOAD_ERROR)
        if data[0] == Configurations.KEYBOARD_DATES_AMOUNT.value:
            try:
                int(data[1])
            except ValueError:
                raise ConfigurationError(CONFIGURATION_VALUE_VALUE_ERROR)

    @classmethod
    def update(cls, data: tuple[str, Optional[str]]) -> Configuration:
        cls.data_is_valid(data)

        config_name: Optional[Enum] = Configurations.get_instance_by_value(data[0])
        if not config_name:
            raise ConfigurationError(CONFIGURATION_WAS_NOT_FOUND_MESSAGE.format(config_name=config_name))

        update_data: dict = database.update(
            cls.__TABLE, data=("value", str(data[1])), condition=("key", config_name.name.lower())
        )
        configuration = Configuration(**update_data)

        for c in cls.CACHED_CONFIGURATIONS:
            if c.id == configuration.id:
                c.value = configuration.value

        return configuration
