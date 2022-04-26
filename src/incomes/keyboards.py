from telebot import types

from configurations import ConfigurationsService
from incomes.models import SalaryAnswers
from keyboards import add_restart_button
from shared.configurations import Configurations
from shared.finances import Currencies


@add_restart_button
def currencies_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for currency in Currencies.values():
        markup.add(types.KeyboardButton(currency))

    return markup


@add_restart_button
def income_sources_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    configuration = ConfigurationsService.get_by_name(Configurations.INCOME_SOURCES.value)
    sources = (configuration.value or "").split(",")

    for source in sources:
        markup.add(types.KeyboardButton(source))

    return markup


@add_restart_button
def salary_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for salary_answer in SalaryAnswers.values():
        markup.add(types.KeyboardButton(salary_answer))

    return markup
