from telebot import types

from config import bot
from incomes.errors import IncomesError
from incomes.keyboards import (
    currencies_keyboard,
    income_sources_keyboard,
    salary_keyboard,
)
from incomes.services import IncomesService
from keyboards import confirmation_keyboard, dates_keyboard, default_keyboard
from shared.errors import user_error_handler
from shared.finances.models import Currencies
from shared.handlers import restart_handler
from shared.incomes import KeyboardButtons


@user_error_handler
@restart_handler
def confirmation(m: types.Message, service: IncomesService):
    processed: bool = service.process_confirmation(m.text)
    message = "Incomes saved" if processed else "Incomes wasn't added"

    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=message)


@user_error_handler
@restart_handler
def set_salary(m: types.Message, service: IncomesService):
    service.set_salary(m.text)
    date = service._date.strftime("%m-%d") if service._date else ""

    if service._salary is None:
        raise IncomesError("Unknown income option")

    next_step_text = "\n".join(
        [
            "Would you like to save this income ❓\n",
            f"Date 👉 {date}",  # type: ignore
            f"Description 👉 {service._name}",
            f"Value 👉 {service._value}",
            f"Currency 👉 {service._currency}",
            f"{m.text}",
        ]
    )

    bot.send_message(m.chat.id, text=next_step_text, reply_markup=confirmation_keyboard())

    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=confirmation,
        service=service,
    )


@user_error_handler
@restart_handler
def set_currency(m: types.Message, service: IncomesService):
    service.set_currency(m.text)

    if not service._currency:
        raise IncomesError("Unknown currency")

    currency = getattr(Currencies, service._currency.upper(), Currencies.UAH)
    next_step_text = "\n".join([f"Currency 👉 {currency.value}", "Is it salary?"])

    bot.send_message(m.chat.id, text=next_step_text, reply_markup=salary_keyboard())

    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_salary,
        service=service,
    )


@user_error_handler
@restart_handler
def set_value(m: types.Message, service: IncomesService):
    service.set_value(m.text)
    bot.send_message(
        m.chat.id,
        text=f"✅ Value added 👉 {m.text}\nNow, please select the currency from the list",
        reply_markup=currencies_keyboard(),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_currency,
        service=service,
    )


@user_error_handler
@restart_handler
def set_name(m: types.Message, service: IncomesService):
    service.set_name(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=f"✅ Name added 👉 {m.text}\nNow, please, enter the value:",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_value,
        service=service,
    )


@user_error_handler
@restart_handler
def set_date(m: types.Message, service: IncomesService):
    service.set_date(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=income_sources_keyboard(),
        text=f"✅Date added 👉 {m.text}\nNow, please, enter the name:",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_name,
        service=service,
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.ADD_INCOME.value}")
@user_error_handler
@restart_handler
def add_incomes(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=dates_keyboard(),
        text="Please, select date from the list",
    )
    service = IncomesService(account_id=m.from_user.id)
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_date,
        service=service,
    )
