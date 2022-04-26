from loguru import logger
from telebot import types

import messages
from analytics.handlers import *  # noqa
from authentication import only_for_members
from config import DEFAULT_SEND_SETTINGS, bot
from configurations.handlers import *  # noqa
from costs.handlers import *  # noqa
from equity.handlers import *  # noqa
from incomes.handlers import *  # noqa
from keyboards import default_keyboard
from shared.handlers import user_error_handler
from users import UsersService


@bot.message_handler(commands=["start"])
@user_error_handler
@only_for_members
def start(m: types.Message):
    user, created = UsersService.save_user(m)
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
@user_error_handler
@only_for_members
def help(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=messages.RESTART_TEXT,
        **DEFAULT_SEND_SETTINGS,
    )
