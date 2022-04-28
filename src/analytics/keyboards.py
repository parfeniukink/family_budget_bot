from telebot import types

from costs import CategoriesService
from keyboards import add_restart_button
from shared.collections import Enum


class AnalyticsOptions(Enum):
    BY_MONTH = "Monthly"
    BY_YEAR = "Annually"


class AnalyticsDetailOptions(Enum):
    BASIC = "Basic"
    DETAILED = "Detailed"


class DetailReportOptions(Enum):
    ALL = "🚛 All"


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


@add_restart_button
def analytics_details_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    markup.add(types.KeyboardButton(DetailReportOptions.ALL.value))

    return markup
