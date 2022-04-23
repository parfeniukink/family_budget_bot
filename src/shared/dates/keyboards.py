from telebot import types

from config import HELP_BUTTON
from shared.dates.services import DatesService


def exist_dates_keyboard(date_format: str = "%Y-%m") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for date in DatesService.get_formatted_dates(date_format):
        markup.add(types.KeyboardButton(date))

    markup.add(HELP_BUTTON)

    return markup
