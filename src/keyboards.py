from datetime import date, timedelta
from itertools import chain
from typing import Callable

from telebot import types

from config import RESTART_BUTTON
from configurations import ConfigurationsService
from configurations.models import Configuration
from shared.analytics import KeyboardButtons as AnalyticsKB
from shared.configurations import Configurations
from shared.configurations import KeyboardButtons as ConfigurationsKB
from shared.costs import KeyboardButtons as CostsKB
from shared.equity import KeyboardButtons as EquityKB
from shared.incomes import KeyboardButtons as IncomesKB


def add_restart_button(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> types.ReplyKeyboardMarkup:
        markup = func(*args, **kwargs)
        markup.add(RESTART_BUTTON)
        return markup

    return inner


@add_restart_button
def default_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for button in chain(
        CostsKB.values(),
        IncomesKB.values(),
        AnalyticsKB.values(),
        EquityKB.values(),
        ConfigurationsKB.values(),
    ):
        markup.add(types.KeyboardButton(button))

    return markup


@add_restart_button
def confirmation_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton("✅ Yes"))
    markup.add(types.InlineKeyboardButton("❌ No"))

    return markup


@add_restart_button
def dates_keyboard() -> types.ReplyKeyboardMarkup:
    DATES_KEYBOARD_AMOUNT: Configuration = ConfigurationsService.get_by_name(
        Configurations.ADD_COSTS_DATES_AMOUNT.name.lower()
    )

    dates = [date.today() - timedelta(days=i) for i in range(int(DATES_KEYBOARD_AMOUNT.value))]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for d in dates:
        markup.add(types.KeyboardButton(str(d)))

    return markup
