from telebot import types

from analytics.domain import (
    AnalyticsDetailLevels,
    AnalyticsError,
    AnalyticsGeneralMenu,
    AnalyticsOptions,
    AnalyticsStorage,
    DetailReportExtraOptions,
    ExtraCallbackData,
)
from analytics.keyboards import (
    analytics_detail_level_keyboard,
    analytics_detail_levels_keyboard,
    analytics_periods_keyboard,
)
from analytics.services import AnalitycsService
from bot import CallbackMessages, bot
from categories import CategoriesService
from configurations.services import ConfigurationsCRUD
from dates import exist_dates_keyboard
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler, restart_handler
from shared.messages import MESSAGE_DEPRICATED
from users import UsersService
from users.services import UsersCRUD

__all__ = ("analytics",)


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.CATEGORY_SELECTED.value))
@base_error_handler
async def category_selected_callback_query(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)

    if storage.option is not AnalyticsOptions.MONTHLY:
        raise AnalyticsError(MESSAGE_DEPRICATED)
    if storage.detail_level is not AnalyticsDetailLevels.DETAILED:
        raise AnalyticsError(MESSAGE_DEPRICATED)
    if not storage.date:
        raise AnalyticsError(MESSAGE_DEPRICATED)

    category_name = q.data.replace(ExtraCallbackData.CATEGORY_SELECTED.value, "")

    await CallbackMessages.delete(q)

    if category_name == DetailReportExtraOptions.ALL.value.name:
        reports = AnalitycsService.get_monthly_detailed_report(storage.date)
        for report in reports:
            await bot.send_message(q.message.chat.id, text=report, **DEFAULT_SEND_SETTINGS)
    else:
        category = CategoriesService.get_by_name(category_name)
        reports = AnalitycsService.get_monthly_detailed_report(storage.date, category)
        for report in reports:
            await bot.send_message(q.message.chat.id, text=report, **DEFAULT_SEND_SETTINGS)


@bot.callback_query_handler(func=lambda c: c.data == AnalyticsDetailLevels.DETAILED.value.callback_data)
@base_error_handler
async def detail_level_selected_callback_query(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)

    if storage.option is not AnalyticsOptions.MONTHLY:
        raise AnalyticsError(MESSAGE_DEPRICATED)

    storage.detail_level = AnalyticsDetailLevels.DETAILED
    await CallbackMessages.edit(
        q=q,
        text="Please select the category",
        reply_markup=analytics_detail_level_keyboard(callback_data=ExtraCallbackData.CATEGORY_SELECTED.value),
    )


@bot.callback_query_handler(func=lambda c: c.data == AnalyticsDetailLevels.BASIC.value.callback_data)
@base_error_handler
async def basic_level_selected_callback_query(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)

    if storage.option is not AnalyticsOptions.MONTHLY:
        raise AnalyticsError(MESSAGE_DEPRICATED)
    if not storage.date:
        raise AnalyticsError(MESSAGE_DEPRICATED)

    storage.detail_level = AnalyticsDetailLevels.BASIC
    new_message = "".join((m for m in AnalitycsService.get_monthly_basic_report(storage.date)))

    await CallbackMessages.edit(q=q, text=new_message)


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.MONTH_SELECTED.value))
@base_error_handler
async def month_selected_callback_query(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)
    if storage.option is not AnalyticsOptions.MONTHLY:
        raise AnalyticsError(MESSAGE_DEPRICATED)

    storage.date = q.data.replace(ExtraCallbackData.MONTH_SELECTED.value, "")

    await CallbackMessages.edit(
        q=q,
        text="Select detail level",
        reply_markup=analytics_detail_levels_keyboard(),
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith(ExtraCallbackData.YEAR_SELECTED.value))
@base_error_handler
async def year_selected_callback_query(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)
    if storage.option is not AnalyticsOptions.ANNUALLY:
        raise AnalyticsError(MESSAGE_DEPRICATED)

    date = q.data.replace(ExtraCallbackData.YEAR_SELECTED.value, "")
    new_message = AnalitycsService.get_annyally_report(date)

    await CallbackMessages.edit(q=q, text=new_message)


@bot.callback_query_handler(func=lambda c: c.data == AnalyticsOptions.MONTHLY.value.callback_data)
@base_error_handler
async def monthly_dispatcher(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)
    storage.option = AnalyticsOptions.MONTHLY
    user = UsersCRUD.fetch_by_account_id(q.from_user.id)
    configuration = ConfigurationsCRUD.fetch(user)

    await CallbackMessages.edit(
        q=q,
        text="Select month from the list",
        reply_markup=exist_dates_keyboard(
            configuration=configuration,
            date_format="%Y-%m",
            callback_data=ExtraCallbackData.MONTH_SELECTED.value,
        ),
    )


@bot.callback_query_handler(func=lambda c: c.data == AnalyticsOptions.ANNUALLY.value.callback_data)
@base_error_handler
async def annually_dispatcher(q: types.CallbackQuery):
    storage: AnalyticsStorage = AnalyticsStorage(q.from_user.id)
    storage.option = AnalyticsOptions.ANNUALLY
    user = UsersCRUD.fetch_by_account_id(q.from_user.id)
    configuration = ConfigurationsCRUD.fetch(user)

    await CallbackMessages.edit(
        q=q,
        text="Select year from the list",
        reply_markup=exist_dates_keyboard(
            configuration=configuration,
            date_format="%Y",
            callback_data=ExtraCallbackData.YEAR_SELECTED.value,
        ),
    )


@bot.message_handler(regexp=rf"^{AnalyticsGeneralMenu.ANALYTICS.value}")
@base_error_handler
@restart_handler
@UsersService.only_for_members
async def analytics(m: types.Message):
    await bot.send_message(
        m.chat.id,
        reply_markup=analytics_periods_keyboard(),
        text="Choose option",
    )
