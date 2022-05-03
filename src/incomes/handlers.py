from telebot import types

from bot import bot
from dates import dates_keyboard
from finances import Currencies
from incomes.domain import IncomesError, IncomesGeneralMenu
from incomes.keyboards import (
    currencies_keyboard,
    income_sources_keyboard,
    salary_keyboard,
)
from incomes.messages import (
    INCOME_DATE_ADDED_MESSAGE,
    INCOME_IS_SALARY_PROMPT,
    INCOME_NAME_ADDED_MESSAGE,
    INCOME_NOT_SAVED_MESSAGE,
    INCOME_OPTION_INVALID_ERROR,
    INCOME_SAVE_CONFIRMATION_MESSAGE,
    INCOME_SAVED_MESSAGE,
    INCOME_VALUE_ADDED_MESSAGE,
    SELECT_DATE_PROMPT,
)
from incomes.services import IncomesService
from shared.domain import base_error_handler, restart_handler
from shared.keyboards import confirmation_keyboard, default_keyboard
from shared.messages import CURRENCY_INVALID_ERROR
from users import UsersService

__all__ = ("add_incomes",)


@base_error_handler
@restart_handler
def confirmation(m: types.Message, service: IncomesService):
    processed: bool = service.process_confirmation(m.text)
    message = INCOME_SAVED_MESSAGE if processed else INCOME_NOT_SAVED_MESSAGE

    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=message)


@base_error_handler
@restart_handler
def set_salary(m: types.Message, service: IncomesService):
    service.set_salary(m.text)
    date = service._date.strftime("%m-%d") if service._date else ""

    if service._salary is None:
        raise IncomesError(INCOME_OPTION_INVALID_ERROR)
    if service._currency is None:
        raise IncomesError(CURRENCY_INVALID_ERROR.format(allowed=Currencies.get_database_values()))

    next_step_text = INCOME_SAVE_CONFIRMATION_MESSAGE.format(
        date=date,
        description=service._name,
        value=service._value,
        currency=getattr(Currencies, service._currency.upper()).value,
        source=m.text,
    )

    bot.send_message(m.chat.id, text=next_step_text, reply_markup=confirmation_keyboard())

    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=confirmation,
        service=service,
    )


@base_error_handler
@restart_handler
def set_currency(m: types.Message, service: IncomesService):
    service.set_currency(m.text)

    if not service._currency:
        raise IncomesError(CURRENCY_INVALID_ERROR.format(allowed=Currencies.get_database_values()))

    currency = getattr(Currencies, service._currency.upper(), Currencies.UAH)

    bot.send_message(
        m.chat.id,
        text=INCOME_IS_SALARY_PROMPT.format(currency=currency.value),
        reply_markup=salary_keyboard(),
    )

    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_salary,
        service=service,
    )


@base_error_handler
@restart_handler
def set_value(m: types.Message, service: IncomesService):
    service.set_value(m.text)
    bot.send_message(
        m.chat.id,
        text=INCOME_VALUE_ADDED_MESSAGE.format(value=m.text),
        reply_markup=currencies_keyboard(),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_currency,
        service=service,
    )


@base_error_handler
@restart_handler
def set_name(m: types.Message, service: IncomesService):
    service.set_name(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=INCOME_NAME_ADDED_MESSAGE.format(name=m.text),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_value,
        service=service,
    )


@base_error_handler
@restart_handler
def set_date(m: types.Message, service: IncomesService):
    service.set_date(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=income_sources_keyboard(),
        text=INCOME_DATE_ADDED_MESSAGE.format(date=m.text),
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_name,
        service=service,
    )


@bot.message_handler(regexp=rf"^{IncomesGeneralMenu.ADD_INCOME.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
def add_incomes(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=dates_keyboard(),
        text=SELECT_DATE_PROMPT,
    )
    service = IncomesService(account_id=m.from_user.id)
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=set_date,
        service=service,
    )
