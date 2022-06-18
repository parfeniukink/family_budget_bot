from datetime import datetime

from telebot import types

from bot import CallbackMessages, bot
from configurations.services import ConfigurationsCRUD
from dates import dates_keyboard
from finances.domain import Currencies
from incomes.domain import (
    ExtraCallbackData,
    IncomesError,
    IncomesGeneralMenu,
    IncomesStorage,
    SalaryAnswers,
)
from incomes.keyboards import income_sources_keyboard, is_salary_keyboard
from incomes.services import IncomesCRUD
from shared.domain import ConfirmationOptions, base_error_handler, restart_handler
from shared.keyboards import (
    confirmation_keyboard,
    currencies_keyboard,
    default_keyboard,
)
from shared.validators import money_value_validator
from storages import State
from users import UsersService
from users.services import UsersCRUD

__all__ = ("add_incomes",)


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.CONFIRMATION_SELECTED.value))
@base_error_handler
async def confirmation_selected_callback_query(q: types.CallbackQuery):
    storage = IncomesStorage(q.from_user.id)
    storage.check_fields("value", "description", "currency", "date", "salary")

    result = q.data.replace(ExtraCallbackData.CONFIRMATION_SELECTED.value, "")
    salary_text = SalaryAnswers.SALARY.value if storage.salary else SalaryAnswers.NOT_SALARY.value

    await CallbackMessages.delete(q)

    if result == ConfirmationOptions.YES.value:
        IncomesCRUD.save(storage)
        text = "\n".join(
            (
                "✅ Money income saved\n\n",
                f"Description 👉 {storage.description}",
                f"Value 👉 {storage.value}",
                f"Currency 👉 {Currencies.get_repr(storage.currency)}",  # type: ignore
                f"Date 👉 {storage.date.strftime('%Y-%m-%d')}",  # type: ignore
                salary_text,
            )
        )
        await bot.send_message(chat_id=q.message.chat.id, text=text, reply_markup=default_keyboard())
    else:
        await bot.send_message(
            chat_id=q.message.chat.id, text="❌ Money income is not saved", reply_markup=default_keyboard()
        )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.IS_SALARY_SELECTED.value))
@base_error_handler
async def is_salary_selected_callback_query(q: types.CallbackQuery):
    storage = IncomesStorage(q.from_user.id)
    storage.check_fields("value", "description", "currency", "date")

    result = q.data.replace(ExtraCallbackData.IS_SALARY_SELECTED.value, "")
    storage.salary = True if result == SalaryAnswers.SALARY.value else False

    text = "\n".join(
        (
            f"Description 👉 {storage.description}",
            f"Value 👉 {storage.value}",
            f"Currency 👉 {Currencies.get_repr(storage.currency)}",  # type: ignore
            f"Date 👉 {storage.date.strftime('%Y-%m-%d')}",  # type: ignore
            result,
            "\nDo you want to save money income?",
        )
    )
    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=confirmation_keyboard(callback_data=ExtraCallbackData.CONFIRMATION_SELECTED.value),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.DATE_SELECTED.value))
@base_error_handler
async def date_selected_callback_query(q: types.CallbackQuery):
    storage = IncomesStorage(q.from_user.id)
    storage.check_fields("value", "description", "currency")

    result = q.data.replace(ExtraCallbackData.DATE_SELECTED.value, "")

    try:
        storage.date = datetime.strptime(result, "%Y-%m-%d")
    except ValueError:
        raise IncomesError("Date format invalid")

    text = "\n".join(
        (
            f"Description 👉 {storage.description}",
            f"Value 👉 {storage.value}",
            f"Currency 👉 {Currencies.get_repr(storage.currency)}",  # type: ignore
            f"Date 👉 {storage.date.strftime('%Y-%m-%d')}",  # type: ignore
            "\nChoose option",
        )
    )
    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=is_salary_keyboard(
            callback_data=ExtraCallbackData.IS_SALARY_SELECTED.value,
        ),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.CURRENCY_SELECTED.value))
@base_error_handler
async def currency_selected_callback_query(q: types.CallbackQuery):
    storage = IncomesStorage(q.from_user.id)
    storage.check_fields("value", "description")

    result = q.data.replace(ExtraCallbackData.CURRENCY_SELECTED.value, "")
    currency = Currencies.get_database_value(result)
    storage.currency = currency

    user = UsersCRUD.fetch_by_account_id(q.from_user.id)
    configuration = ConfigurationsCRUD.fetch(user)

    text = "\n".join(
        (
            f"Description 👉 {storage.description}",
            f"Value 👉 {storage.value}",
            f"Currency 👉 {Currencies.get_repr(currency)}",
            "\nSelect date:",
        )
    )
    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=dates_keyboard(
            configuration=configuration,
            callback_data=ExtraCallbackData.DATE_SELECTED.value,
        ),
    )


@base_error_handler
async def description_entered_callback(m: types.Message):
    storage = IncomesStorage(m.from_user.id)
    storage.trash_messages.add(m.id)
    storage.check_fields("value")

    for message in storage.trash_messages:
        await bot.delete_message(m.chat.id, message)
    storage.trash_messages.clear()

    text = "\n".join(
        (
            f"Description 👉 {storage.description}",
            f"Value 👉 {storage.value}",
            "\nSelect currency:",
        )
    )
    await bot.send_message(
        text=text,
        chat_id=m.chat.id,
        reply_markup=currencies_keyboard(callback_data=ExtraCallbackData.CURRENCY_SELECTED.value),
    )


@base_error_handler
async def value_entered_callback(m: types.Message):
    storage = IncomesStorage(m.from_user.id)
    state = State(m.from_user.id)
    state.set(storage=storage, key="description", validator=None, callback=description_entered_callback)

    user = UsersCRUD.fetch_by_account_id(m.from_user.id)
    configuration = ConfigurationsCRUD.fetch(user)

    storage.trash_messages.add(m.id)
    sent_message = await bot.send_message(
        text="Enter the description and press Enter",
        chat_id=m.chat.id,
        reply_markup=income_sources_keyboard(configuration),
    )
    storage.trash_messages.add(sent_message.id)


@bot.message_handler(regexp=rf"^{IncomesGeneralMenu.ADD_INCOME.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
async def add_incomes(m: types.Message):

    storage = IncomesStorage(m.from_user.id)
    state = State(m.from_user.id)
    state.set(storage=storage, key="value", validator=money_value_validator, callback=value_entered_callback)

    sent_message = await bot.send_message(
        text="Enter the value and press Enter",
        chat_id=m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    storage.trash_messages.add(sent_message.id)
