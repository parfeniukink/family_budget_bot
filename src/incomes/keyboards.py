from telebot import types

from configurations import ConfigurationsService
from shared.configurations import Configurations


def imcome_sources_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    configuration = ConfigurationsService.get_by_name(Configurations.INCOME_SOURCES.value)
    sources = (configuration.value or "").split(" ")

    for source in sources:
        markup.add(types.KeyboardButton(source))

    return markup
