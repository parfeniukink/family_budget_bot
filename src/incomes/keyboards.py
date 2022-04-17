from telebot import types

from configurations import ConfigurationsService
from shared.configurations import Configurations
from shared.finances import Currencies


def currencies_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for currency in Currencies.values():
        markup.add(types.KeyboardButton(currency))

    return markup


def income_sources_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    configuration = ConfigurationsService.get_by_name(Configurations.INCOME_SOURCES.value)
    sources = (configuration.value or "").split(" ")

    for source in sources:
        markup.add(types.KeyboardButton(source))

    return markup
