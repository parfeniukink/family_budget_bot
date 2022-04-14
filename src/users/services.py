from typing import Optional

from telebot import types

from config import database
from db import DatabaseError
from users.models import User


class UsersService:
    USERS_TABLE = "users"

    @classmethod
    def fetch_user(cls, account_id: int) -> Optional[User]:
        data = database.fetch(cls.USERS_TABLE, "account_id", account_id)
        return User(**data) if data else None

    @classmethod
    def _save_user(cls, m: types.Message) -> None:
        data = {
            "account_id": m.from_user.id,
            "chat_id": m.chat.id,
            "username": m.from_user.username,
            "full_name": m.from_user.full_name,
        }
        database.insert("users", data)

    @classmethod
    def save_user(cls, m: types.Message) -> tuple[User, bool]:
        """Return user instance and created information"""
        user: Optional[User] = cls.fetch_user(m.from_user.id)
        if user:
            return user, False

        cls._save_user(m)

        created_user: Optional[User] = cls.fetch_user(m.from_user.id)

        if not created_user:
            raise DatabaseError("For some reason we can not create a new user in database. Check connection.")

        return created_user, True
