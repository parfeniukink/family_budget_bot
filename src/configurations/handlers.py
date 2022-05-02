from telebot import types

import messages
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
from configurations.services import ConfigurationsService
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler, restart_handler
from shared.keyboards import default_keyboard
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
        text=messages.CONFIGURATION_UPDATED.format(
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
        raise ConfigurationError(messages.CONFIGURATION_INVALID)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=messages.CONFIGURATION_ENTER_PROMPT,
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
        raise ConfigurationError("Invalid option")
    if m.text == ConfigurationsMenu.UPDATE.value:
        bot.send_message(
            m.chat.id,
            reply_markup=configurations_update_keyboard(),
            text="Please, select the configuration ⬇️",
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
        text="What do you want to do?",
        **DEFAULT_SEND_SETTINGS,
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_action,
    )
