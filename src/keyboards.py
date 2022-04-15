from telebot import types

from shared.costs import KeyboardButtons


def default_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/help"))
    for button in KeyboardButtons.values():
        markup.add(types.KeyboardButton(button))

    return markup


def decline_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/stop"))
    return markup


def confirmation_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton("✅ Yes"))
    markup.add(types.InlineKeyboardButton("❌ No"))

    return markup
