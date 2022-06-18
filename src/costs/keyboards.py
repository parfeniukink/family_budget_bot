from typing import Iterable

from telebot import types

from configurations import Configuration
from costs.domain import Cost
from shared.keyboards import add_restart_button


@add_restart_button
def cost_sources_keyboard(configuration: Configuration) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sources = [item for el in (configuration.cost_sources or "").split(",") if (item := el.strip())]

    for source in sources:
        markup.add(types.KeyboardButton(source))

    return markup


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
