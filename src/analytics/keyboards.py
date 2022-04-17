from telebot import types

from analytics.services import AnalitycsService
from config import HELP_BUTTON
from shared.collections import Enum


class AnalyticsOptions(Enum):
    BY_MONTH = "By month"


class AnalyticsDetailOptions(Enum):
    BASIC = "Basic"
    DETAILED = "Detailed"


def analytics_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in AnalyticsOptions.values():
        markup.add(types.KeyboardButton(choise))

    markup.add(HELP_BUTTON)

    return markup


def analytics_dates_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for date in AnalitycsService.get_formatted_dates():
        markup.add(types.KeyboardButton(date))

    return markup


def analytics_dates_detail_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in AnalyticsDetailOptions.values():
        markup.add(types.KeyboardButton(choise))

    markup.add(HELP_BUTTON)

    return markup
