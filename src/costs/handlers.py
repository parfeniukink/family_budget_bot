from telebot import types

from bot import bot
from categories import categories_keyboard
from costs.domain import Cost, CostsError, CostsGeneralMenu
from costs.keyboards import ids_keyboard
from costs.messages import (
    COST_ADD_CATEGORY_SELECT_PROMPT,
    COST_ADD_CATEGORY_SELECTED_MESSAGE,
    COST_ADD_CONFIRMATION_MESSAGE,
    COST_ADD_DATE_SELECTED_MESSAGE,
    COST_DELETE_CATEGORY_SELECTED_MESSAGE,
    COST_DELETE_DATE_SELECTED_MESSAGE,
    COST_DELETE_MONTH_SELECT_PROMPT,
    COST_DELETED_MESSAGE,
    COST_DESCRIPTION_ADDED_MESSAGE,
    COST_NOT_FOUND_FOR_CATEGORY_MESSAGE,
    COST_NOT_SAVED_MESSAGE,
    COST_SAVED_MESSAGE,
    NO_MONTH_SELECTED_ERROR,
)
from costs.services import CostsService
from dates import dates_keyboard, exist_dates_keyboard
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler, restart_handler
from shared.formatting import get_number_in_frames
from shared.keyboards import confirmation_keyboard, default_keyboard
from shared.messages import CATEGORY_NOT_SELECTED_ERROR
from users import UsersService

__all__ = ("add_costs", "delete_costs")


#####################################################
# Add costs
#####################################################
@base_error_handler
@restart_handler
def confirmation(m: types.Message, costs_service: CostsService):
    processed: bool = costs_service.process_confirmation(m.text)
    message = COST_SAVED_MESSAGE if processed else COST_NOT_SAVED_MESSAGE

    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=message)


@base_error_handler
@restart_handler
def add_value(m: types.Message, costs_service: CostsService):
    costs_service.add_value(m.text)
    category = costs_service._category.name if costs_service._category else ""
    date = costs_service._date.strftime("%m-%d") if costs_service._date else ""
    next_step_text = COST_ADD_CONFIRMATION_MESSAGE.format(
        date=date,
        category=category,
        description=costs_service._text,
        value=get_number_in_frames(
            costs_service._value,
        ),
    )
    bot.send_message(
        m.chat.id,
        reply_markup=confirmation_keyboard(),
        text=next_step_text,
        **DEFAULT_SEND_SETTINGS,
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=confirmation,
        costs_service=costs_service,
    )


@base_error_handler
@restart_handler
def add_text(m: types.Message, costs_service: CostsService):
    costs_service.add_text(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=COST_DESCRIPTION_ADDED_MESSAGE.format(description=m.text),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=add_value,
        costs_service=costs_service,
    )


@base_error_handler
@restart_handler
def select_date(m: types.Message, costs_service: CostsService):
    costs_service.set_date(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=COST_ADD_DATE_SELECTED_MESSAGE.format(date=m.text),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=add_text,
        costs_service=costs_service,
    )


@base_error_handler
@restart_handler
def select_category(m: types.Message, costs_service: CostsService):
    costs_service.set_category(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=dates_keyboard(),
        text=COST_ADD_CATEGORY_SELECTED_MESSAGE.format(category=m.text),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_date,
        costs_service=costs_service,
    )


@bot.message_handler(regexp=rf"^{CostsGeneralMenu.ADD_COST.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
def add_costs(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=categories_keyboard(),
        text=COST_ADD_CATEGORY_SELECT_PROMPT,
    )
    costs_service = CostsService(account_id=m.from_user.id)

    bot.register_next_step_handler_by_chat_id(chat_id=m.chat.id, callback=select_category, costs_service=costs_service)


#####################################################
# Delete costs
#####################################################
@base_error_handler
@restart_handler
def select_id_for_delete(m: types.Message, service: CostsService, allowed_ids: set[int]):
    service.delete_by_id(str(m.text), allowed_ids)
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=COST_DELETED_MESSAGE,
    )


@base_error_handler
@restart_handler
def select_category_for_delete(m: types.Message, service: CostsService, costs: list[Cost]):
    service.set_category(m.text)
    if not service._category:
        raise CostsError(CATEGORY_NOT_SELECTED_ERROR)

    filtered_costs = [cost for cost in costs if cost.category_id == service._category.id]
    if not filtered_costs:
        bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=COST_NOT_FOUND_FOR_CATEGORY_MESSAGE.format(cost=m.text),
        )
    else:
        fcosts = service.get_formatted_costs_for_delete(filtered_costs)

        bot.send_message(
            m.chat.id,
            reply_markup=ids_keyboard(reversed(filtered_costs)),
            text=COST_DELETE_CATEGORY_SELECTED_MESSAGE.format(
                category=m.text,
                costs=fcosts,
            ),
            **DEFAULT_SEND_SETTINGS,
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=m.chat.id,
            callback=select_id_for_delete,
            service=service,
            allowed_ids={cost.id for cost in filtered_costs},
        )


@base_error_handler
@restart_handler
def select_month_for_delete(m: types.Message, service: CostsService):
    if not m.text:
        raise CostsError(NO_MONTH_SELECTED_ERROR)

    costs: dict[str, list[Cost]] = service.get_monthly_costs(m.text)
    merged_costs = [el for key in costs for el in costs[key]]

    bot.send_message(
        m.chat.id,
        reply_markup=categories_keyboard(),
        text=COST_DELETE_DATE_SELECTED_MESSAGE.format(month=m.text),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_category_for_delete,
        service=service,
        costs=merged_costs,
    )


@bot.message_handler(regexp=rf"^{CostsGeneralMenu.DELETE_COST.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
def delete_costs(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=exist_dates_keyboard(),
        text=COST_DELETE_MONTH_SELECT_PROMPT,
    )
    service = CostsService(account_id=m.from_user.id)

    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_month_for_delete,
        service=service,
    )
