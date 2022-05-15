from contextlib import suppress
from functools import wraps
from typing import Callable, Optional

from loguru import logger
from telebot import types

from db import DatabaseError, database
from settings import ALLOWED_USER_ACCOUNT_IDS
from shared.domain import BaseError
from users.domain import User, UsersError

__all__ = ("UsersService", "UsersCRUD")


class UsersCache:
    _USERS: dict[int, User] = {}

    @classmethod
    def set(cls, key: int, value: User):
        cls._USERS[key] = value

    @classmethod
    def get(cls, key) -> Optional[User]:
        with suppress(KeyError):
            return cls._USERS[key]
        return None


class UsersCRUD:
    USERS_TABLE = "users"

    @classmethod
    def fetch_by_id(cls, id: int) -> Optional[User]:
        if cache_user := UsersCache.get(id):
            return cache_user

        data = database.fetchone(cls.USERS_TABLE, "id", id)
        logger.debug("Users table injected")

        user = User(**data) if data else None

        if not user:
            return None

        UsersCache.set(id, user)

        return user

    @classmethod
    def fetch_by_account_id(cls, account_id: int) -> User:
        if cache_user := UsersCache.get(account_id):
            return cache_user

        data = database.fetchone(cls.USERS_TABLE, "account_id", account_id)
        logger.debug("Users table injected")

        if not data:
            raise UsersError(f"No such user with id {account_id}")

        user = User(**data)
        UsersCache.set(account_id, user)

        return user

    @classmethod
    def save_user(cls, m: types.Message) -> tuple[User, bool]:
        """Return user instance and created information"""
        with suppress(UsersError):
            user: Optional[User] = cls.fetch_by_account_id(m.from_user.id)
            return user, False

        payload = {
            "account_id": m.from_user.id,
            "chat_id": m.chat.id,
            "username": m.from_user.username,
            "full_name": m.from_user.full_name,
        }
        data: dict = database.insert("users", payload)
        created_user = User(**data)

        if not created_user:
            raise DatabaseError("For some reason we can not create a new user in database. Check connection.")

        return created_user, True


class UsersService:
    @staticmethod
    def only_for_members(coro: Callable) -> Callable:
        """
        Check if user id is present in the allowed list.
        Use as decorator for handlers
        """

        @wraps(coro)
        async def inner(m: types.Message, *args, **kwargs):
            if str(m.from_user.id) not in ALLOWED_USER_ACCOUNT_IDS:
                raise BaseError("Sorry, you have not access to this Bot")
            return await coro(m, *args, **kwargs)

        return inner
