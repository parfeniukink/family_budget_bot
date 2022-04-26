from telebot import types

from keyboards import add_restart_button
from shared.dates.services import DatesService


@add_restart_button
def exist_dates_keyboard(date_format: str = "%Y-%m") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for date in DatesService.get_formatted_dates(date_format):
        markup.add(types.KeyboardButton(date))

    return markup
