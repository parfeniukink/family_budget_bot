from telebot import types

from configurations import Configuration
from incomes.domain import SalaryAnswers
from shared.keyboards import add_restart_button


@add_restart_button
def income_sources_keyboard(configuration: Configuration) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    sources = (configuration.income_sources or "").split(",")

    for source in sources:
        markup.add(types.KeyboardButton(source))

    return markup


def is_salary_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(text=item, callback_data="".join((callback_data, item)))
            for item in SalaryAnswers.values()
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)
