from contextlib import suppress
from datetime import datetime

from telebot import types

from bot import CallbackMessages, bot
from categories import categories_keyboard
from categories.services import CategoriesService
from configurations.domain import Configuration
from configurations.services import ConfigurationsCRUD
from costs.domain import (
    Cost,
    CostsError,
    CostsGeneralMenu,
    CostsStorage,
    ExtraCallbackData,
)
from costs.keyboards import ids_keyboard
from costs.services import CostsCRUD, CostsService
from dates import dates_keyboard, exist_dates_keyboard
from finances import Currencies
from shared.domain import ConfirmationOptions, base_error_handler
from shared.keyboards import confirmation_keyboard, default_keyboard
from shared.messages import MESSAGE_DEPRICATED
from shared.validators import money_value_validator
from storages import State
from users import User, UsersCRUD, UsersService

__all__ = ("delete_costs", "add_costs")


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.ADD_CONFIRMATION_SELECTED.value))
@base_error_handler
async def add_confirmation_selected_callback_query(q: types.CallbackQuery):
    storage = CostsStorage(q.from_user.id)
    storage.check_fields("category", "value", "description", "date")
    result = q.data.replace(ExtraCallbackData.ADD_CONFIRMATION_SELECTED.value, "")

    user: User = UsersCRUD.fetch_by_account_id(q.from_user.id)
    configuration: Configuration = ConfigurationsCRUD.fetch(user)

    await CallbackMessages.delete(q)

    if result == ConfirmationOptions.YES.value:
        CostsService.save_costs(storage)
        text = (
            "✅ Cost saved\n\n"
            f"Description 👉 {storage.description}\n"
            f"Value 👉 {storage.value}\n"
            f"Currency 👉 {Currencies.get_repr(configuration.default_currency)}\n"
            f"Category 👉 {storage.category.name}\n"  # type: ignore
            f"Date 👉 {storage.date.strftime('%Y-%m-%d')}"  # type: ignore
        )
        await bot.send_message(chat_id=q.message.chat.id, text=text, reply_markup=default_keyboard())
    else:
        await bot.send_message(chat_id=q.message.chat.id, text="❌ Cost is not saved", reply_markup=default_keyboard())


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.ADD_MONTH_SELECTED.value))
@base_error_handler
async def date_add_selected_callback_query(q: types.CallbackQuery):
    storage = CostsStorage(q.from_user.id)
    storage.check_fields("category", "value", "description")

    date = q.data.replace(ExtraCallbackData.ADD_MONTH_SELECTED.value, "")

    try:
        storage.date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise CostsError("Date format invalid")

    text = (
        f"Description 👉 {storage.description}\n"
        f"Value 👉 {storage.value}\n"
        f"Category 👉 {storage.category.name}\n"  # type: ignore
        f"Date 👉 {date}\n\n"
        f"Do you want to save costs?"
    )

    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=confirmation_keyboard(callback_data=ExtraCallbackData.ADD_CONFIRMATION_SELECTED.value),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.ADD_CATEGORYADD_SELECTED.value))
@base_error_handler
async def category_add_selected_callback_query(q: types.CallbackQuery):
    storage = CostsStorage(q.from_user.id)
    category_name = q.data.replace(ExtraCallbackData.ADD_CATEGORYADD_SELECTED.value, "")
    storage.category = CategoriesService.get_by_name(category_name)

    user = UsersCRUD.fetch_by_account_id(q.from_user.id)
    configuration = ConfigurationsCRUD.fetch(user)

    text = (
        f"Description 👉 {storage.description}\n"
        f"Value 👉 {storage.value}\n"
        f"Category 👉 {storage.category.name}\n\n"
        f"Select date"
    )

    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=dates_keyboard(
            configuration=configuration,
            callback_data=ExtraCallbackData.ADD_MONTH_SELECTED.value,
        ),
    )


@base_error_handler
async def description_entered_callback(m: types.Message):
    storage = CostsStorage(m.from_user.id)
    storage.trash_messages.add(m.id)

    for message in storage.trash_messages:
        with suppress(Exception):
            await bot.delete_message(m.chat.id, message)

    text = f"Description 👉 {storage.description}\nValue 👉 {storage.value}\n\nSelect category:"

    await bot.send_message(
        text=text,
        chat_id=m.chat.id,
        reply_markup=categories_keyboard(
            callback_data=ExtraCallbackData.ADD_CATEGORYADD_SELECTED.value,
        ),
    )


@base_error_handler
async def value_entered_callback(m: types.Message):
    storage = CostsStorage(m.from_user.id)
    state = State(m.from_user.id)
    state.set(storage=storage, key="description", validator=None, callback=description_entered_callback)

    storage.trash_messages.add(m.id)
    sent_message = await bot.send_message(
        text="Enter the description and press Enter",
        chat_id=m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    storage.trash_messages.add(sent_message.id)


@bot.message_handler(regexp=rf"^{CostsGeneralMenu.ADD_COST.value}")
@base_error_handler
@UsersService.only_for_members
async def add_costs(m: types.Message):
    storage = CostsStorage(m.from_user.id)
    state = State(m.from_user.id)
    state.set(storage=storage, key="value", validator=money_value_validator, callback=value_entered_callback)

    sent_message = await bot.send_message(
        text="Enter the value and press Enter",
        chat_id=m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    storage.trash_messages.add(sent_message.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.DEL_CONFIRMATION_SELECTED.value))
@base_error_handler
async def del_confirmation_selected_callback_query(q: types.CallbackQuery):
    confirm = q.data.replace(ExtraCallbackData.DEL_CONFIRMATION_SELECTED.value, "")
    if confirm == ConfirmationOptions.NO.value:
        await CallbackMessages.edit(q=q, text="❌ Canceled")
    else:
        storage = CostsStorage(q.from_user.id)
        if storage.delete_id is None:
            raise CostsError(MESSAGE_DEPRICATED)

        CostsService.delete_by_id(storage.delete_id)

        await CallbackMessages.edit(q=q, text="✅ Cost deleted")


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.COST_ID_SELECTED.value))
@base_error_handler
async def id_to_delete_selected_callback_query(q: types.CallbackQuery):
    storage = CostsStorage(q.from_user.id)
    storage.delete_id = q.data.replace(ExtraCallbackData.COST_ID_SELECTED.value, "")

    if storage.delete_id is None:
        raise CostsError("id to delete is not set")

    cost: Cost | None = CostsCRUD.get_by_id(storage.delete_id)

    if cost is None:
        raise CostsError("Nu such cost in database")

    text = "\n".join(
        (
            "Do you realy want to delete cost?\n",
            f"Date 👉 {cost.date.strftime('%Y-%m-%d')}",
            f"Description 👉 {cost.name}",
            f"Value 👉 {cost.value}",
            f"Currency 👉 {Currencies.get_repr(cost.currency)}",
        )
    )
    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=confirmation_keyboard(
            callback_data=ExtraCallbackData.DEL_CONFIRMATION_SELECTED.value,
        ),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.DEL_CATEGORY_SELECTED.value))
@base_error_handler
async def del_category_selected_callback_query(q: types.CallbackQuery):
    storage = CostsStorage(q.from_user.id)

    if storage.costs is None:
        raise CostsError(MESSAGE_DEPRICATED)

    category_name = q.data.replace(ExtraCallbackData.DEL_CATEGORY_SELECTED.value, "")
    storage.category = CategoriesService.get_by_name(category_name)
    filtered_costs = [cost for cost in storage.costs if cost.category_id == storage.category.id]

    if not filtered_costs:
        await CallbackMessages.edit(q=q, text="✅ No costs in this category", reply_markup=default_keyboard()),

    else:
        await CallbackMessages.edit(
            q=q,
            text="Please select cost you want to delete",
            reply_markup=ids_keyboard(
                costs=filtered_costs,
                callback_data=ExtraCallbackData.COST_ID_SELECTED.value,
            ),
        )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.DEL_MONTH_SELECTED.value))
@base_error_handler
async def month_selected_callback_query(q: types.CallbackQuery):
    storage = CostsStorage(q.from_user.id)
    service = CostsService(account_id=q.from_user.id)

    date = q.data.replace(ExtraCallbackData.DEL_MONTH_SELECTED.value, "")
    costs: dict[str, list[Cost]] = service.get_monthly_costs(date)
    storage.costs = [el for key in costs for el in costs[key]]

    await CallbackMessages.edit(
        q=q,
        reply_markup=categories_keyboard(
            callback_data=ExtraCallbackData.DEL_CATEGORY_SELECTED.value,
        ),
        text="Please select the category",
    )


@bot.message_handler(regexp=rf"^{CostsGeneralMenu.DELETE_COST.value}")
@base_error_handler
@UsersService.only_for_members
async def delete_costs(m: types.Message):
    storage = CostsStorage(m.from_user.id)
    storage.clean()

    user = UsersCRUD.fetch_by_account_id(m.from_user.id)
    configuration = ConfigurationsCRUD.fetch(user)

    await bot.send_message(
        text="Please select month",
        chat_id=m.chat.id,
        reply_markup=exist_dates_keyboard(
            configuration=configuration,
            date_format="%Y-%m",
            callback_data=ExtraCallbackData.DEL_MONTH_SELECTED.value,
        ),
    )
