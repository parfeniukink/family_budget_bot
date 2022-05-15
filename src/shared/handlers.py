from loguru import logger
from telebot import types

from bot import bot
from configurations.services import ConfigurationsCRUD
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler, restart_handler
from shared.keyboards import default_keyboard
from shared.messages import LINE_ITEM, USER_CREATED_MESSAGE, USER_EXISTS_MESSAGE
from storages import State
from users import UsersCRUD, UsersService


@bot.message_handler(commands=["start"])
@base_error_handler
@UsersService.only_for_members
async def start(m: types.Message):
    user, created = UsersCRUD.save_user(m)
    if created:
        ConfigurationsCRUD.startup_population(user)
        logger.success(LINE_ITEM.format(key="Created a new user", value=user.username))
        logger.success(f"Configuration created for user {user.username}")
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


@bot.message_handler(func=lambda _: True)
@base_error_handler
@restart_handler
async def all_messages(m):
    state = State(m.from_user.id)

    if not state.storage or not state.key or not state.callback:
        return await bot.send_message(m.chat.id, "Please use keyboard")

    if state.validator:
        state.validator(m.text)

    setattr(state.storage, state.key, m.text)
    next_callback = state.callback
    state.clean()

    return await next_callback(m)
