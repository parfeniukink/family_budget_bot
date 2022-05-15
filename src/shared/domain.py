from enum import Enum as _Enum
from enum import IntEnum as _IntEnum
from enum import unique
from functools import wraps
from typing import Callable, Generator, Iterable, Optional, Union
from uuid import uuid4

from loguru import logger
from pydantic import BaseModel, Extra
from pydantic.fields import Field
from telebot import types

from bot import CallbackMessages, bot
from settings import DEFAULT_SEND_SETTINGS, RESTART_BUTTON_TEXT
from shared.keyboards import default_keyboard
from shared.messages import RESTART


class BaseError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Adding costs error"
        super().__init__(message, *args, **kwargs)


def restart_handler(coro: Callable):
    """
    Handler to cover any handler or callback for aboarting if `/restart` was entered
    Use only for functions with first Message parameter
    """

    @wraps(coro)
    async def inner(m: types.Message, *args, **kwargs):
        if m.text == RESTART_BUTTON_TEXT:
            await bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=RESTART)
        else:
            return await coro(m, *args, **kwargs)

    return inner


def base_error_handler(coro: Callable) -> Callable:
    """
    This decorator could be used only for handlers.
    m: Union[types.Message, types.CallbackQuery] is mandatory first argument
    """

    @wraps(coro)
    async def inner(m: Union[types.Message, types.CallbackQuery], *args, **kwargs) -> Optional[types.Message]:

        regular_message = isinstance(m, types.Message)
        chat_id = m.chat.id if regular_message else m.message.chat.id

        try:
            return await coro(m, *args, **kwargs)
        except BaseError as err:
            logger.error(err)
            message = f"<b>⚠️ Error:</b>\n\n{err}"
            if not regular_message:
                return await CallbackMessages.edit(q=m, text=message)
            else:
                return await bot.send_message(
                    chat_id, reply_markup=default_keyboard(), text=message, **DEFAULT_SEND_SETTINGS
                )

    return inner


@unique
class Enum(_Enum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]

    @classmethod
    def names(cls: Iterable) -> list:
        return [i.name for i in cls]


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


def _uuid_facory() -> Generator:
    items = set()

    while True:
        item = str(uuid4())[:15]

        if item not in items:
            items.add(item)
            yield item
        else:
            continue


uuid_facory = _uuid_facory()


def random_uuid() -> str:
    return next(uuid_facory)


class CallbackItem(Model):
    name: str
    callback_data: str = Field(default_factory=random_uuid)


class ConfirmationOptions(Enum):
    YES = "✅ Yes"
    NO = "❌ No"


class PaginationOptions(Enum):
    RIGHT = "Right"
    LEFT = "Left"
