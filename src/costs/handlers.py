from telebot import types

from config import bot
from configurations import configuration_error_handler
from costs.keyboards import categories_keyboard
from costs.services import CostsService
from keyboards import confirmation_keyboard, dates_keyboard, default_keyboard
from shared.costs import KeyboardButtons
from shared.errors import user_error_handler


@user_error_handler
@configuration_error_handler
def confirmation(m: types.Message, costs_service: CostsService):
    processed: bool = costs_service.process_confirmation(m.text)
    message = "Costs saved" if processed else "Costs wasn't added"

    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=message)


@user_error_handler
def add_value(m: types.Message, costs_service: CostsService):
    costs_service.add_value(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=confirmation_keyboard(),
        text=f"Value added: {m.text}\nWoud you like to save this Cost?",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=confirmation,
        costs_service=costs_service,
    )


@user_error_handler
def add_text(m: types.Message, costs_service: CostsService):
    costs_service.add_text(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=f"Description added: {m.text}\nEnter the value",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=add_value,
        costs_service=costs_service,
    )


@user_error_handler
def select_date(m: types.Message, costs_service: CostsService):
    costs_service.set_date(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=f"Date: {m.text}\nEnter the description",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=add_text,
        costs_service=costs_service,
    )


@user_error_handler
def select_category(m: types.Message, costs_service: CostsService):
    costs_service.set_category(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=dates_keyboard(),
        text=f"Selected {m.text} category",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_date,
        costs_service=costs_service,
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.ADD_COST.value}")
@user_error_handler
def add_costs(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=categories_keyboard(),
        text="Select category",
    )
    costs_service = CostsService(account_id=m.from_user.id)

    bot.register_next_step_handler_by_chat_id(chat_id=m.chat.id, callback=select_category, costs_service=costs_service)
