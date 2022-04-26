from typing import Iterable

from telebot import types

from costs.models import Cost
from costs.services import CategoriesService
from keyboards import add_restart_button


@add_restart_button
def categories_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    return markup


@add_restart_button
def ids_keyboard(costs: Iterable[Cost]) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for cost in costs:
        markup.add(types.KeyboardButton(str(cost.id)))

    return markup
