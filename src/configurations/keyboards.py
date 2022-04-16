from telebot import types

from shared.collections import Enum
from shared.configurations import Configurations


class ConfigurationMenu(Enum):
    GET_ALL = "Get all configurations"
    UPDATE = "Update"


def configurations_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in ConfigurationMenu.values():
        markup.add(types.KeyboardButton(choise))

    return markup


def configurations_update_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for configuration in Configurations:
        markup.add(types.KeyboardButton(configuration.value))

    return markup
