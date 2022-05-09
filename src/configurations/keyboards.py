from telebot import types

from configurations.domain import Configurations, ConfigurationsMenu


def configurations_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(
                text=item.name,
                callback_data=item.callback_data,
            ),
        ]
        for item in ConfigurationsMenu.values()
    ]
    return types.InlineKeyboardMarkup(keyboard)


def configurations_edit_keyboard(callback_data: str) -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(
                text=item.value,
                callback_data="".join((callback_data, item.name)),
            ),
        ]
        for item in Configurations
    ]

    return types.InlineKeyboardMarkup(keyboard)
