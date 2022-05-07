from datetime import date, timedelta

from telebot import types

from configurations import Configuration, Configurations, ConfigurationsService
from dates.services import DatesService


def dates_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    DATES_KEYBOARD_AMOUNT: Configuration = ConfigurationsService.get_by_name(
        Configurations.KEYBOARD_DATES_AMOUNT.name.lower()
    )

    dates = [date.today() - timedelta(days=i) for i in range(int(DATES_KEYBOARD_AMOUNT.value))]

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


def exist_dates_keyboard(*_, date_format: str = "%Y-%m", callback_data: str) -> types.InlineKeyboardMarkup:
    keyboard = [
        [types.InlineKeyboardButton(text=fdate, callback_data="".join((callback_data, fdate)))]
        for fdate in DatesService.get_formatted_dates(date_format)
    ]
    return types.InlineKeyboardMarkup(keyboard)
