from itertools import chain
from typing import Callable

from telebot import types

from settings import RESTART_BUTTON_TEXT


def add_restart_button(func: Callable) -> Callable:
    """Add restart button to any function that returns ReplyKeyboardMarkup"""

    def inner(*args, **kwargs) -> types.ReplyKeyboardMarkup:
        markup = func(*args, **kwargs)
        markup.add(types.KeyboardButton(RESTART_BUTTON_TEXT))

        return markup

    return inner


@add_restart_button
def default_keyboard() -> types.ReplyKeyboardMarkup:
    from analytics import AnalyticsGeneralMenu
    from configurations import ConfigurationsGeneralMenu
    from costs import CostsGeneralMenu
    from equity import EquityGeneralMenu
    from incomes import IncomesGeneralMenu

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for button in chain(
        CostsGeneralMenu.values(),
        IncomesGeneralMenu.values(),
        AnalyticsGeneralMenu.values(),
        EquityGeneralMenu.values(),
        ConfigurationsGeneralMenu.values(),
    ):
        markup.add(types.KeyboardButton(button))

    return markup


@add_restart_button
def confirmation_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton("✅ Yes"))
    markup.add(types.InlineKeyboardButton("❌ No"))

    return markup
