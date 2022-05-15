from datetime import date, timedelta
from itertools import islice

from telebot import types

from configurations import Configuration
from dates.services import DatesService


def dates_keyboard(configuration: Configuration, callback_data: str) -> types.InlineKeyboardMarkup:
    dates = (date.today() - timedelta(days=i) for i in range(configuration.keyboard_dates_amount))

    keyboard = [
        [
            types.InlineKeyboardButton(
                text=str(fdate),
                callback_data="".join((callback_data, str(fdate))),
            )
        ]
        for fdate in dates
    ]

    return types.InlineKeyboardMarkup(keyboard)


def exist_dates_keyboard(
    *_, configuration: Configuration, date_format: str = "%Y-%m", callback_data: str
) -> types.InlineKeyboardMarkup:
    keyboard = [
        [types.InlineKeyboardButton(text=fdate, callback_data="".join((callback_data, fdate)))]
        for fdate in islice(
            DatesService.get_formatted_dates(date_format),
            configuration.keyboard_dates_amount,
        )
    ]
    return types.InlineKeyboardMarkup(keyboard)
