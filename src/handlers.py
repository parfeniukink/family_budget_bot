from loguru import logger
from telebot import types

import messages
from config import DEFAULT_SEND_SETTINGS, bot
from keyboards import default_keyboard
from users import UsersService


@bot.message_handler(commands=["start"])
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


@bot.message_handler(commands=["help"])
def help(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=messages.HELP_TEXT,
        **DEFAULT_SEND_SETTINGS,
    )


@bot.message_handler(commands=["stop"])
def stop(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text="Operation permitted",
        **DEFAULT_SEND_SETTINGS,
    )
