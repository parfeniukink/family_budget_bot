from typing import Iterable

from telebot import types

from config import HELP_BUTTON
from costs.models import Cost
from costs.services import CategoriesService


def categories_keyboard() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in CategoriesService.CACHED_CATEGORIES:
        markup.add(types.KeyboardButton(category.name))

    markup.add(HELP_BUTTON)

    return markup


def ids_keyboard(costs: Iterable[Cost]) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for cost in costs:
        markup.add(types.KeyboardButton(str(cost.id)))

    markup.add(HELP_BUTTON)

    return markup
