from loguru import logger
from telebot import types

import messages
from bot import bot
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler
from shared.keyboards import default_keyboard
from users import UsersCRUD


@bot.message_handler(commands=["start"])
@base_error_handler
def start(m: types.Message):
    user, created = UsersCRUD.save_user(m)
    if created:
        logger.success(f"Created new user -> {user.username}")
        bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=messages.USER_CREATED,
            **DEFAULT_SEND_SETTINGS,
        )
    else:
        logger.info(f"User exists -> {user.username}")
        bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=messages.USER_EXISTS,
            **DEFAULT_SEND_SETTINGS,
        )


@bot.message_handler(commands=["restart"])
@base_error_handler
def restart(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=messages.RESTART,
        **DEFAULT_SEND_SETTINGS,
    )
