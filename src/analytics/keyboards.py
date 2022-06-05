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
            types.InlineKeyboardButton(text=item.name, callback_data=item.callback_data)
            for item in AnalyticsOptions.values()
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)


def analytics_detail_levels_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(text=item.name, callback_data=item.callback_data)
            for item in AnalyticsDetailLevels.values()
        ]
    ]
    return types.InlineKeyboardMarkup(keyboard)


def analytics_detail_level_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    markup = categories_keyboard(callback_data)

    # NOTE: Add `Only incomes` button
    markup.add(
        types.InlineKeyboardButton(
            text=DetailReportExtraOptions.INCOMES.value.name,
            callback_data="".join((callback_data, DetailReportExtraOptions.INCOMES.value.name)),
        )
    )

    # NOTE: Add `All categories` button
    markup.add(
        types.InlineKeyboardButton(
            text=DetailReportExtraOptions.ALL.value.name,
            callback_data="".join((callback_data, DetailReportExtraOptions.ALL.value.name)),
        )
    )
    return markup
