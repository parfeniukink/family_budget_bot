from functools import wraps

from telebot import types

from config import HELP_TEXT, bot
from keyboards import default_keyboard


def restart_handler(func):
    """
    Handler to cover any handler or callback for aboarting if `/restart` was entered
    Use only for functions with first Message parameter
    """

    @wraps(func)
    def inner(m: types.Message, *args, **kwargs):
        if m.text == HELP_TEXT:
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text="⚠️ Aboarted",
            )
        else:
            return func(m, *args, **kwargs)

    return inner
