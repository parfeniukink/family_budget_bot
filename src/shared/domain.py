from enum import Enum as _Enum
from enum import IntEnum as _IntEnum
from enum import unique
from functools import wraps
from typing import Callable, Iterable, Optional

from loguru import logger
from pydantic import BaseModel, Extra
from telebot import types

from bot import bot
from settings import DEFAULT_SEND_SETTINGS, RESTART_BUTTON_TEXT
from shared.keyboards import default_keyboard
from shared.messages import ABORTED


class BaseError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Adding costs error"
        super().__init__(message, *args, **kwargs)


def restart_handler(func):
    """
    Handler to cover any handler or callback for aboarting if `/restart` was entered
    Use only for functions with first Message parameter
    """

    @wraps(func)
    def inner(m: types.Message, *args, **kwargs):
        if m.text == RESTART_BUTTON_TEXT:
            bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=ABORTED)
        else:
            return func(m, *args, **kwargs)

    return inner


def base_error_handler(func) -> Callable:
    """
    This decorator could be used only for handlers.
    m: types.Message is mandatory first argument
    """

    @wraps(func)
    def inner(m: types.Message, *args, **kwargs) -> None:
        try:
            return func(m, *args, **kwargs)
        except BaseError as err:
            logger.error(err)
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text=f"<b>⚠️ Error:</b>\n\n{err}",
                **DEFAULT_SEND_SETTINGS,
            )

    return inner


@unique
class Enum(_Enum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]


@unique
class IntEnum(_IntEnum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]

    @classmethod
    def names(cls: Iterable) -> list:
        return [i.name for i in cls]


class Model(BaseModel):
    class Config:
        extra = Extra.ignore
        orm_mode = True
        use_enum_values = True
        allow_population_by_field_name = True
        validate_assignment = True
