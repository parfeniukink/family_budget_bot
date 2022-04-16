from telebot import types

from config import bot
from incomes.errors import incomes_eror_handler
from incomes.keyboards import imcome_sources_keyboard
from incomes.services import IncomesService
from keyboards import confirmation_keyboard, dates_keyboard, default_keyboard
from shared.incomes import KeyboardButtons


@incomes_eror_handler
def confirmation(m: types.Message, service: IncomesService):
    processed: bool = service.process_confirmation(m.text)
    message = "Incomes saved" if processed else "Incomes wasn't added"

    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=message)


@incomes_eror_handler
def set_value(m: types.Message, service: IncomesService):
    service.set_value(m.text)
    bot.send_message(m.chat.id, text=f"Value: {m.text}\n\nPlease confirm:", reply_markup=confirmation_keyboard())
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=confirmation,
        service=service,
    )


@incomes_eror_handler
def set_name(m: types.Message, service: IncomesService):
    service.set_name(m.text)
    bot.send_message(
        m.chat.id,
        text=f"Name: {m.text}\n\nEnter the value:",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_value,
        service=service,
    )


@incomes_eror_handler
def set_date(m: types.Message, service: IncomesService):
    service.set_date(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=f"Date: {m.text}\n\nEnter the name:",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_name,
        service=service,
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.ADD_INCOME.value}")
@incomes_eror_handler
def add_incomes(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=dates_keyboard(),
        text="Select date",
    )
    service = IncomesService(account_id=m.from_user.id)
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_date,
        service=service,
    )
