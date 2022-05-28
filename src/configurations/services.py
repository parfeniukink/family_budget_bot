from contextlib import suppress
from typing import Optional

from loguru import logger

from configurations.domain import (
    Configuration,
    ConfigurationError,
    Configurations,
    ConfigurationsStorage,
)
from db import database
from finances.domain import Currencies
from shared.messages import LINE_ITEM
from users.domain import User
from users.services import UsersCRUD

__all__ = ("ConfigurationsService", "ConfigurationsCRUD")


class ConfigurationsCache:
    _CONFIGURATIONS: dict[User, Configuration] = {}

    @classmethod
    def set(cls, user: User, configuration: Configuration):
        cls._CONFIGURATIONS[user] = configuration

    @classmethod
    def get(cls, user: User) -> Optional[Configuration]:
        with suppress(KeyError):
            return cls._CONFIGURATIONS[user]
        return None


class ConfigurationsCRUD:
    __TABLE = "configurations"

    @classmethod
    def fetch(cls, user: User) -> Configuration:
        if cached_configuration := ConfigurationsCache.get(user):
            return cached_configuration

        data: Optional[dict] = database.fetchone(cls.__TABLE, column="user_id", value=user.id)
        if not data:
            raise ConfigurationError(
                f"There is no configuration for user {user.username}. Please contact to developers"
            )

        configuration = Configuration(**data)
        ConfigurationsCache.set(user, configuration)

        logger.debug("Configurations table injected")
        return configuration

    @classmethod
    def update(cls, account_id: int, storage: ConfigurationsStorage) -> Configuration:
        user = UsersCRUD.fetch_by_account_id(account_id)
        if not storage.configuration_name or not storage.value:
            raise ConfigurationError("Configuration update payload is not full")

        update_data: dict = database.update(
            cls.__TABLE,
            data=(storage.configuration_name, storage.value),
            condition=("user_id", user.id),  # type: ignore
        )
        configuration: Configuration = Configuration(**update_data)
        ConfigurationsCache.set(user, configuration)

        logger.debug("Configurations table injected")
        return configuration

    @classmethod
    def startup_population(cls, user: User) -> Configuration:
        payload = {
            "default_currency": Currencies.get_database_value("BYN"),
            "income_sources": "",
            "keyboard_dates_amount": 5,
            "user_id": user.id,
        }
        data: dict = database.insert(cls.__TABLE, payload)

        configuration = Configuration(**data)
        ConfigurationsCache.set(user, configuration)

        logger.debug("Configurations table injected")
        return configuration


class ConfigurationsService:
    @classmethod
    def get_all_formatted(cls, account_id: int) -> str:
        user: User = UsersCRUD.fetch_by_account_id(account_id)
        configuration: Configuration = ConfigurationsCRUD.fetch(user)

        return "\n\n".join(
            (
                [
                    LINE_ITEM.format(key=conf.value, value=getattr(configuration, conf.name.lower()))
                    for conf in Configurations
                ]
            )
        )
