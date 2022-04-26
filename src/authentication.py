from typing import Callable

from telebot import types

from config import ALLOWED_USER_ACCOUNT_IDS
from shared.errors import UserError


def only_for_members(func) -> Callable:
    def inner(m: types.Message, *args, **kwargs):
        if str(m.from_user.id) not in ALLOWED_USER_ACCOUNT_IDS:
            raise UserError("Sorry, you have not access to this Bot")
        return func(m, *args, **kwargs)

    return inner
