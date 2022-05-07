from telebot import types

from analytics.domain import (
    AnalyticsDetailLevels,
    AnalyticsOptions,
    DetailReportExtraOptions,
)
from categories import categories_keyboard


def analytics_periods_keyboard():
    keyboard = [
        [
            types.InlineKeyboardButton(
                text=AnalyticsOptions.MONTHLY.value.name, callback_data=AnalyticsOptions.MONTHLY.value.callback_data
            ),
            types.InlineKeyboardButton(
                text=AnalyticsOptions.ANNUALLY.value.name, callback_data=AnalyticsOptions.ANNUALLY.value.callback_data
            ),
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)


def analytics_detail_levels_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(text=item.value.name, callback_data=item.value.callback_data),
        ]
        for item in AnalyticsDetailLevels
    ]
    return types.InlineKeyboardMarkup(keyboard)


def analytics_detail_level_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    markup = categories_keyboard(callback_data)
    markup.add(
        types.InlineKeyboardButton(
            text=DetailReportExtraOptions.ALL.value.name,
            callback_data="".join((callback_data, DetailReportExtraOptions.ALL.value.name)),
        )
    )
    return markup
