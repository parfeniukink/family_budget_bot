from telebot import types

from categories.services import CategoriesService
from shared.keyboards import add_restart_button


@add_restart_button
def categories_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    return markup
