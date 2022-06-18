from telebot import types

from categories.services import CategoriesService


def categories_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(text=category.name, callback_data="".join((callback_data, category.name))),
        ]
        for category in CategoriesService.get_ordered()
    ]
    return types.InlineKeyboardMarkup(keyboard)
