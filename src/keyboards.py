from telebot import types

from costs import KeyboardButtons


def default_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/help"))
    for button in KeyboardButtons.values():
        markup.add(types.KeyboardButton(button))

    return markup
