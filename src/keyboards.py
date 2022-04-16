from datetime import date, timedelta

from telebot import types

from config import DATES_KEYBOARD_LEN
from shared.configurations import KeyboardButtons as ConfigurationsKB
from shared.costs import KeyboardButtons as CostsKB
from shared.incomes import KeyboardButtons as IncomesKB


def default_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/help"))
    for button in CostsKB.values():
        markup.add(types.KeyboardButton(button))
    for button in IncomesKB.values():
        markup.add(types.KeyboardButton(button))
    for button in ConfigurationsKB.values():
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


def dates_keyboard() -> types.ReplyKeyboardMarkup:
    dates = [date.today() - timedelta(days=i) for i in range(DATES_KEYBOARD_LEN)]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for d in dates:
        markup.add(types.KeyboardButton(str(d)))

    return markup
