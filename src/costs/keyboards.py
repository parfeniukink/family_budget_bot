from telebot import types

from config import HELP_BUTTON
from costs.services import CategoriesService


def categories_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    markup.add(HELP_BUTTON)

    return markup
