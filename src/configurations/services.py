from config import database
from configurations.errors import ConfigurationError
from configurations.models import Configuration


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
    CACHED_CONFIGURATIONS: list[Configuration]

    @classmethod
    def get_by_name(cls, name: str) -> Configuration:
        for configuration in cls.CACHED_CONFIGURATIONS:
            if configuration.key == name:
                return configuration
        raise ConfigurationError(f"No such confuguration {name}")
