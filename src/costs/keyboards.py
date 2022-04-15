from datetime import date, timedelta

from telebot import types

from config import DATES_KEYBOARD_LEN
from costs.services import CategoriesService


def categories_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    return markup


def dates_keyboard() -> types.ReplyKeyboardMarkup:
    dates = [date.today() - timedelta(days=i) for i in range(DATES_KEYBOARD_LEN)]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for d in dates:
        markup.add(types.KeyboardButton(str(d)))

    return markup
