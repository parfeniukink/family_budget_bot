from typing import Callable, Optional

from telebot import types

from db import DatabaseError, database
from settings import ALLOWED_USER_ACCOUNT_IDS
from shared.domain import BaseError
from users.domain import User

__all__ = ("UsersService", "UsersCRUD")


class UsersService:
    @staticmethod
    def only_for_members(func) -> Callable:
        """
        Check if user id is present in the allowed list.
        Use as decorator for handlers
        """

        def inner(m: types.Message, *args, **kwargs):
            if str(m.from_user.id) not in ALLOWED_USER_ACCOUNT_IDS:
                raise BaseError("Sorry, you have not access to this Bot")
            return func(m, *args, **kwargs)

        return inner


class UsersCRUD:
    USERS_TABLE = "users"

    @classmethod
    def fetch_by_id(cls, id: int) -> Optional[User]:
        data = database.fetch(cls.USERS_TABLE, "id", id)
        return User(**data) if data else None

    @classmethod
    def fetch_by_account_id(cls, account_id: int) -> Optional[User]:
        data = database.fetch(cls.USERS_TABLE, "account_id", account_id)
        return User(**data) if data else None

    @classmethod
    def save_user(cls, m: types.Message) -> tuple[User, bool]:
        """Return user instance and created information"""
        user: Optional[User] = cls.fetch_by_account_id(m.from_user.id)
        if user:
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
