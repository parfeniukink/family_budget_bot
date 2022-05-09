from datetime import date, timedelta

from telebot import types

from configurations import Configuration, Configurations, ConfigurationsService
from dates.services import DatesService
from shared.keyboards import add_restart_button


@add_restart_button
def dates_keyboard() -> types.ReplyKeyboardMarkup:
    DATES_KEYBOARD_AMOUNT: Configuration = ConfigurationsService.get_by_name(
        Configurations.KEYBOARD_DATES_AMOUNT.name.lower()
    )

    dates = [date.today() - timedelta(days=i) for i in range(int(DATES_KEYBOARD_AMOUNT.value))]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for d in dates:
        markup.add(types.KeyboardButton(str(d)))

    return markup


@add_restart_button
def exist_dates_keyboard(date_format: str = "%Y-%m") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for fdate in DatesService.get_formatted_dates(date_format):
        markup.add(types.KeyboardButton(fdate))

    return markup
