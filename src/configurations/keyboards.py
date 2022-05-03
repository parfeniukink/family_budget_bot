from telebot import types

from configurations.domain import Configurations, ConfigurationsMenu
from shared.keyboards import add_restart_button


@add_restart_button
def configurations_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in ConfigurationsMenu.values():
        markup.add(types.KeyboardButton(choise))

    return markup


@add_restart_button
def configurations_update_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for configuration in Configurations:
        markup.add(types.KeyboardButton(configuration.value))

    return markup
