from telebot import types

from bot import bot
from configurations.domain import (
    ConfigurationError,
    Configurations,
    ConfigurationsGeneralMenu,
    ConfigurationsMenu,
)
from configurations.keyboards import (
    configurations_keyboard,
    configurations_update_keyboard,
)
from configurations.messages import (
    CONFIGURATION_ENTER_PROMPT,
    CONFIGURATION_INVALID_MESSAGE,
    CONFIGURATION_SELCT_MESSAGE,
    CONFIGURATION_UPDATED_MESSAGE,
)
from configurations.services import ConfigurationsService
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler, restart_handler
from shared.keyboards import default_keyboard
from shared.messages import BASE_QUESTION, INVAID_OPTION_MESSAGE
from users import UsersService

__all__ = ("configurations",)


@base_error_handler
@restart_handler
@UsersService.only_for_members
def update_configuration(m: types.Message, name: str):
    configuration = ConfigurationsService.update(data=(name, m.text))
    configuration_name = getattr(Configurations, configuration.key.upper()).value
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=CONFIGURATION_UPDATED_MESSAGE.format(
            configuration_name=configuration_name,
            configuration_value=configuration.value,
        ),
        **DEFAULT_SEND_SETTINGS,
    )


@base_error_handler
@restart_handler
@UsersService.only_for_members
def select_configuration(m: types.Message):
    if m.text not in Configurations.values():
        raise ConfigurationError(CONFIGURATION_INVALID_MESSAGE)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=CONFIGURATION_ENTER_PROMPT,
        **DEFAULT_SEND_SETTINGS,
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=update_configuration,
        name=m.text,
    )


@base_error_handler
@restart_handler
def select_action(m: types.Message):
    if m.text not in ConfigurationsMenu.values():
        raise ConfigurationError(INVAID_OPTION_MESSAGE)
    if m.text == ConfigurationsMenu.UPDATE.value:
        bot.send_message(
            m.chat.id,
            reply_markup=configurations_update_keyboard(),
            text=CONFIGURATION_SELCT_MESSAGE,
            **DEFAULT_SEND_SETTINGS,
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=m.chat.id,
            callback=select_configuration,
        )
    else:
        configurations = ConfigurationsService.get_all_formatted()
        bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=configurations,
            **DEFAULT_SEND_SETTINGS,
        )


@bot.message_handler(regexp=rf"^{ConfigurationsGeneralMenu.CONFIGURATIONS.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
def configurations(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=configurations_keyboard(),
        text=BASE_QUESTION,
        **DEFAULT_SEND_SETTINGS,
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_action,
    )
