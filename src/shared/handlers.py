from functools import wraps

from loguru import logger
from telebot import types

from config import DEFAULT_SEND_SETTINGS, RESTART_BUTTON_TEXT, bot
from keyboards import default_keyboard
from shared.errors import UserError


def restart_handler(func):
    """
    Handler to cover any handler or callback for aboarting if `/restart` was entered
    Use only for functions with first Message parameter
    """

    @wraps(func)
    def inner(m: types.Message, *args, **kwargs):
        if m.text == RESTART_BUTTON_TEXT:
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text="⚠️ Aborted",
            )
        else:
            return func(m, *args, **kwargs)

    return inner


def user_error_handler(func):
    """
    This decorator could be used only for handlers.
    m: types.Message is mandatory first argument
    """

    def inner(m: types.Message, *args, **kwargs):
        try:
            return func(m, *args, **kwargs)
        except UserError as err:
            logger.error(err)
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text=f"<b>⚠️ Error:</b>\n\n{err}",
                **DEFAULT_SEND_SETTINGS,
            )

    return inner
