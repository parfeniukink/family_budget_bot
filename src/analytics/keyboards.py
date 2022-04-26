from telebot import types

from keyboards import add_restart_button
from shared.collections import Enum


class AnalyticsOptions(Enum):
    BY_MONTH = "Monthly"
    BY_YEAR = "Annually"


class AnalyticsDetailOptions(Enum):
    BASIC = "Basic"
    DETAILED = "Detailed"


@add_restart_button
def analytics_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in AnalyticsOptions.values():
        markup.add(types.KeyboardButton(choise))

    return markup


@add_restart_button
def analytics_dates_detail_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in AnalyticsDetailOptions.values():
        markup.add(types.KeyboardButton(choise))

    return markup
