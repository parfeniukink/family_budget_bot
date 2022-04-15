from typing import Optional

from loguru import logger
from telebot import types

from config import DEFAULT_SEND_SETTINGS, bot
from keyboards import default_keyboard


class CostsError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Adding costs error"
        super().__init__(message, *args, **kwargs)


def costs_eror_handler(func):
    """
    This decorator could be used only for handlers.
    m: types.Message is mandatory first argument
    """

    def inner(m: types.Message, *args, **kwargs):
        try:
            return func(m, *args, **kwargs)
        except CostsError as err:
            logger.error(err)
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text=f"<b>Error:</b>\n\n{err}",
                **DEFAULT_SEND_SETTINGS,
            )

    return inner
