from loguru import logger
from telebot import types

from bot import bot
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler
from shared.keyboards import default_keyboard
from shared.messages import LINE_ITEM
from startup.messages import USER_CREATED_MESSAGE, USER_EXISTS_MESSAGE
from users import UsersCRUD, UsersService


@bot.message_handler(commands=["start"])
@base_error_handler
@UsersService.only_for_members
async def start(m: types.Message):
    user, created = UsersCRUD.save_user(m)
    if created:
        logger.success(LINE_ITEM.format(key="Created a new user", value=user.username))
        await bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=USER_CREATED_MESSAGE,
            **DEFAULT_SEND_SETTINGS,
        )
    else:
        logger.info(LINE_ITEM.format(key="User exists", value=user.username))
        await bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=USER_EXISTS_MESSAGE,
            **DEFAULT_SEND_SETTINGS,
        )
