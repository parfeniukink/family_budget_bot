from typing import Optional

from config import database
from configurations.errors import ConfigurationError
from configurations.models import Configuration
from shared.configurations.constants import Configurations, DefaultCurrencies


class ConfigurationsCache(type):
    CONFIGURATIONS_TABLE = "configurations"

    @classmethod
    def get_configurations(cls) -> list[Configuration]:
        return [Configuration(**item) for item in database.fetchall(cls.CONFIGURATIONS_TABLE)]

    def __getattr__(cls, attr):
        if attr == "CACHED_CONFIGURATIONS":
            data = cls.get_configurations()
            setattr(cls, attr, data)
            return data
        raise AttributeError(attr)


class ConfigurationsService(metaclass=ConfigurationsCache):
    TABLE = "configurations"
    CACHED_CONFIGURATIONS: list[Configuration]

    @classmethod
    def get_by_name(cls, name: str) -> Configuration:
        for configuration in cls.CACHED_CONFIGURATIONS:
            if configuration.key == name:
                return configuration
        raise ConfigurationError(f"No such confuguration {name}")

    @classmethod
    def get_all_formatted(cls) -> str:
        configurations = "\n".join([f"{c.key}: {c.value}" for c in cls.CACHED_CONFIGURATIONS])
        return f"Active configuratoins:\n\n{configurations}"

    @classmethod
    def data_is_valid(cls, data: tuple[str, Optional[str]]) -> None:
        if len(data) != 2:
            raise ConfigurationError("Invalid configuratoin update payload")
        if data[0] not in Configurations.values():
            raise ConfigurationError("Invalid configuratoin selected")

        if data[0] == Configurations.DEFAULT_CURRENCY.value and data[1] not in DefaultCurrencies.values():
            raise ConfigurationError("Invalid currency")

    @classmethod
    def update(cls, data: tuple[str, Optional[str]]) -> Configuration:
        cls.data_is_valid(data)
        if len(data) > 2:
            raise ConfigurationError("Invalid configuratoin update payload")

        update_data: dict = database.update(cls.TABLE, data=("value", data[1]), condition=("key", data[0]))
        configuration = Configuration(**update_data)

        for c in cls.CACHED_CONFIGURATIONS:
            if c.id == configuration.id:
                c.value = configuration.value

        return configuration
