from telebot import types

from configurations import Configurations, ConfigurationsService
from incomes.domain import SalaryAnswers
from shared.keyboards import add_restart_button


@add_restart_button
def income_sources_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    configuration = ConfigurationsService.get_by_name(
        Configurations.INCOME_SOURCES.name.lower(),
    )
    sources = (configuration.value or "").split(",")

    for source in sources:
        markup.add(types.KeyboardButton(source))

    return markup


def is_salary_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(text=item, callback_data="".join((callback_data, item))),
        ]
        for item in SalaryAnswers.values()
    ]
    return types.InlineKeyboardMarkup(keyboard)
