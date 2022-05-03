from telebot import types

from analytics.domain import (
    AnalyticsDetailLevels,
    AnalyticsOptions,
    DetailReportExtraOptions,
)
from categories import CategoriesService
from shared.keyboards import add_restart_button


@add_restart_button
def analytics_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in AnalyticsOptions.values():
        markup.add(types.KeyboardButton(choise))

    return markup


@add_restart_button
def analytics_detail_level_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for choise in AnalyticsDetailLevels.values():
        markup.add(types.KeyboardButton(choise))

    return markup


@add_restart_button
def analytics_detailed_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    markup.add(types.KeyboardButton(DetailReportExtraOptions.ALL.value))

    return markup
