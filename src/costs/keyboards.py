from typing import Iterable

from telebot import types

from costs.domain import Cost


def ids_keyboard(costs: Iterable[Cost], callback_data: str) -> types.InlineKeyboardMarkup:
    keyboard = [
        [
            types.InlineKeyboardButton(
                text=" ".join((f"({cost.date.strftime('%m-%d')})", cost.name, "👉", str(cost.value))),
                callback_data="".join((callback_data, str(cost.id))),
            ),
        ]
        for cost in costs
    ]
    return types.InlineKeyboardMarkup(keyboard)
