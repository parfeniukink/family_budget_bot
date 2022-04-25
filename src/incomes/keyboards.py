from telebot import types

from config import HELP_BUTTON
from configurations import ConfigurationsService
from incomes.models import SalaryAnswers
from shared.configurations import Configurations
from shared.finances import Currencies


def currencies_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for currency in Currencies.values():
        markup.add(types.KeyboardButton(currency))

    markup.add(HELP_BUTTON)

    return markup


def income_sources_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    configuration = ConfigurationsService.get_by_name(Configurations.INCOME_SOURCES.value)
    sources = (configuration.value or "").split(" ")

    for source in sources:
        markup.add(types.KeyboardButton(source))

    markup.add(HELP_BUTTON)

    return markup


def salary_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for salary_answer in SalaryAnswers.values():
        markup.add(types.KeyboardButton(salary_answer))

    markup.add(HELP_BUTTON)

    return markup
