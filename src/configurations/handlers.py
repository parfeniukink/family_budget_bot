from contextlib import suppress

from telebot import types

from bot import CallbackMessages, bot
from configurations.domain import (
    Configuration,
    Configurations,
    ConfigurationsGeneralMenu,
    ConfigurationsMenu,
    ConfigurationsStorage,
    ExtraCallbackData,
)
from configurations.keyboards import (
    configurations_edit_keyboard,
    configurations_keyboard,
)
from configurations.services import ConfigurationsService
from configurations.validators import configurations_validator_dispatcher
from finances.domain import Currencies
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import ConfirmationOptions, base_error_handler, restart_handler
from shared.keyboards import (
    confirmation_keyboard,
    currencies_keyboard,
    default_keyboard,
)
from shared.messages import BASE_QUESTION
from storages import State
from users import UsersService

__all__ = ("configurations",)


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.CONFIRMATION_SELECTED.value))
@base_error_handler
async def confirmation_selected_callback_query(q: types.CallbackQuery):
    storage = ConfigurationsStorage(q.from_user.id)
    storage.check_fields("configuration", "value")
    result = q.data.replace(ExtraCallbackData.CONFIRMATION_SELECTED.value, "")

    storage.trash_messages.add(q.message.id)

    for message in storage.trash_messages:
        with suppress(Exception):
            await bot.delete_message(chat_id=q.message.chat.id, message_id=message)

    if result == ConfirmationOptions.YES.value:
        configuration: Configuration = ConfigurationsService.update(storage)
        configuration_repr: Configurations = getattr(Configurations, storage.configuration.key.upper())  # type: ignore

        text = "\n\n".join(
            (
                "✅ Configuration saved",
                f"{configuration_repr.value} 👉 {configuration.value}",
            )
        )
        await bot.send_message(
            chat_id=q.message.chat.id,
            text=text,
            reply_markup=default_keyboard(),
            **DEFAULT_SEND_SETTINGS,
        )
    else:
        await bot.send_message(
            chat_id=q.message.chat.id,
            text="❌ Configuration is not saved",
            reply_markup=default_keyboard(),
            **DEFAULT_SEND_SETTINGS,
        )


@base_error_handler
async def value_entered_callback(m: types.Message):
    storage = ConfigurationsStorage(m.from_user.id)
    storage.check_fields("configuration", "value")
    storage.trash_messages.add(m.id)
    configuration_repr = getattr(Configurations, storage.configuration.key.upper())  # type: ignore

    text = "\n\n".join(
        (
            "Do you want to update the configuration?",
            f"{configuration_repr.value} 👉 {storage.value}",  # type: ignore
        )
    )

    await bot.send_message(
        text=text,
        chat_id=m.chat.id,
        reply_markup=confirmation_keyboard(callback_data=ExtraCallbackData.CONFIRMATION_SELECTED.value),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.CURRENCY_SELECTED.value))
@base_error_handler
async def currency_selected_callback_query(q: types.CallbackQuery):
    storage = ConfigurationsStorage(q.from_user.id)
    storage.check_fields("configuration")

    result = q.data.replace(ExtraCallbackData.CURRENCY_SELECTED.value, "")
    storage.value = Currencies.get_database_value(result)
    configuration_repr = getattr(Configurations, storage.configuration.key.upper())  # type: ignore
    currency = getattr(Currencies, storage.value.upper())  # type: ignore

    text = "\n\n".join(
        (
            "Do you want to update the configuration?",
            f"{configuration_repr.value} 👉 {currency.value}",  # type: ignore
        )
    )
    await CallbackMessages.edit(
        q=q,
        text=text,
        reply_markup=confirmation_keyboard(
            callback_data=ExtraCallbackData.CONFIRMATION_SELECTED.value,
        ),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.CONFIGURATION_SELECTED.value))
@base_error_handler
async def configuration_selected_callback_query(q: types.CallbackQuery):
    storage = ConfigurationsStorage(q.from_user.id)
    state = State(q.from_user.id)
    configuration_name = q.data.replace(ExtraCallbackData.CONFIGURATION_SELECTED.value, "").lower()
    storage.configuration = ConfigurationsService.get_by_name(configuration_name)

    if configuration_name == Configurations.DEFAULT_CURRENCY.name.lower():
        return await CallbackMessages.edit(
            q=q,
            text="Please select currency",
            reply_markup=currencies_keyboard(
                callback_data=ExtraCallbackData.CURRENCY_SELECTED.value,
            ),
        )

    # NOTE: Setup new state
    state.set(
        storage=storage,
        key="value",
        validator=configurations_validator_dispatcher(storage.configuration),
        callback=value_entered_callback,
    )

    await CallbackMessages.delete(q)

    sent_message = await bot.send_message(
        text="Enter the new value and press Enter",
        chat_id=q.message.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    storage.trash_messages.add(sent_message.id)


@bot.callback_query_handler(func=lambda c: c.data == ConfigurationsMenu.EDIT.value.callback_data)
@base_error_handler
async def edit_configurations_selected_callback_query(q: types.CallbackQuery):
    await CallbackMessages.edit(
        q=q,
        text="Please, select which configuration do you want to edit",
        reply_markup=configurations_edit_keyboard(
            callback_data=ExtraCallbackData.CONFIGURATION_SELECTED.value,
        ),
    )


@bot.callback_query_handler(func=lambda c: c.data == ConfigurationsMenu.GET_ALL.value.callback_data)
@base_error_handler
async def get_all_configurations_selected_callback_query(q: types.CallbackQuery):
    configurations = ConfigurationsService.get_all_formatted()

    await CallbackMessages.delete(q)
    await bot.send_message(
        chat_id=q.message.chat.id,
        text=configurations,
        **DEFAULT_SEND_SETTINGS,
    )


@bot.message_handler(regexp=rf"^{ConfigurationsGeneralMenu.CONFIGURATIONS.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
async def configurations(m: types.Message):
    await bot.send_message(
        m.chat.id,
        reply_markup=configurations_keyboard(),
        text=BASE_QUESTION,
        **DEFAULT_SEND_SETTINGS,
    )
