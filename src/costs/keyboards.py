from typing import Iterable

from telebot import types

from costs.domain import Cost
from shared.keyboards import add_restart_button


@add_restart_button
def ids_keyboard(costs: Iterable[Cost]) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for cost in costs:
        markup.add(types.KeyboardButton(str(cost.id)))

    return markup
