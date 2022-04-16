from telebot import types

from config import bot
from configurations.errors import ConfigurationError
from configurations.keyboards import (
    ConfigurationMenu,
    configurations_keyboard,
    configurations_update_keyboard,
)
from configurations.services import ConfigurationsService
from keyboards import default_keyboard
from shared.configurations.constants import Configurations
from shared.configurations.keyboards import KeyboardButtons


def update_configuration(m: types.Message, name: str):
    configuration = ConfigurationsService.update(data=(name, m.text))
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=f"Configuration updated {configuration.key}: {configuration.value}",
    )


def select_configuration(m: types.Message):
    if m.text not in Configurations.values():
        raise ConfigurationError("Invalid configuration selected")
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text="Enter new value for configuration",
    )
    bot.register_next_step_handler_by_chat_id(chat_id=m.chat.id, callback=update_configuration, name=m.text)


def select_action(m: types.Message):
    if m.text not in ConfigurationMenu.values():
        raise ConfigurationError("Invalid action")
    if m.text == ConfigurationMenu.UPDATE.value:
        bot.send_message(
            m.chat.id,
            reply_markup=configurations_update_keyboard(),
            text="Enter new value for configuration",
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
        )


@bot.message_handler(regexp=rf"^{KeyboardButtons.CONFIGURATIONS.value}")
def configurations(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=configurations_keyboard(),
        text="What do you want to do?",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_action,
    )