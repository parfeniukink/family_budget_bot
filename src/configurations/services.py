from configurations.domain import (
    Configuration,
    ConfigurationError,
    Configurations,
    ConfigurationsStorage,
)
from db import database
from shared.messages import LINE_ITEM

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
        raise ConfigurationError(f"Can not find configuration {name} in database")

    @classmethod
    def get_all_formatted(cls) -> str:
        return "\n\n".join(
            (
                [
                    LINE_ITEM.format(key=getattr(Configurations, c.key.upper()).value, value=c.value)
                    for c in cls.CACHED_CONFIGURATIONS
                ]
            )
        )

    @classmethod
    def update(cls, storage: ConfigurationsStorage) -> Configuration:
        update_data: dict = database.update(
            cls.__TABLE,
            data=("value", storage.value),
            condition=("key", storage.configuration.key),  # type: ignore
        )
        configuration = Configuration(**update_data)

        for c in cls.CACHED_CONFIGURATIONS:
            if c.id == configuration.id:
                c.value = configuration.value

        return configuration
