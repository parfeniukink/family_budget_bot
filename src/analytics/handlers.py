from datetime import datetime

from telebot import types

from analytics.errors import AnalyticsError
from analytics.keyboards import (
    AnalyticsDetailOptions,
    AnalyticsOptions,
    DetailReportOptions,
    analytics_dates_detail_keyboard,
    analytics_details_keyboard,
    analytics_keyboard,
)
from analytics.services import AnalitycsService
from authentication import only_for_members
from config import DEFAULT_SEND_SETTINGS, bot
from costs.services import CategoriesService
from keyboards import default_keyboard
from shared.analytics import KeyboardButtons
from shared.dates import exist_dates_keyboard
from shared.handlers import restart_handler, user_error_handler

__all__ = ("analytics",)


@user_error_handler
@restart_handler
def detailed_option_dispatcher(m: types.Message, month: str):
    no_such_category_error = AnalyticsError(f"Not such category 👉 {m.text}\nPlease use keyboard below")
    category_name = m.text

    if not category_name:
        raise no_such_category_error

    if category_name == DetailReportOptions.ALL.value:
        report = AnalitycsService.get_monthly_detailed_report(month)
        for text in report:
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text=text,
                **DEFAULT_SEND_SETTINGS,
            )
        return

    if category_name not in {c.name for c in CategoriesService.CACHED_CATEGORIES}:
        raise no_such_category_error

    category = CategoriesService.get_by_name(category_name)
    report = AnalitycsService.get_monthly_detailed_report(month, category)

    for text in report:
        bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=text,
            **DEFAULT_SEND_SETTINGS,
        )


@user_error_handler
@restart_handler
def monthly_dispatcher(m: types.Message, month: str):
    if m.text not in AnalyticsDetailOptions.values():
        raise AnalyticsError()

    report = ""

    if m.text == AnalyticsDetailOptions.BASIC.value:
        report = AnalitycsService.get_monthly_basic_report(month)
        for text in report:
            bot.send_message(
                m.chat.id,
                reply_markup=default_keyboard(),
                text=text,
                **DEFAULT_SEND_SETTINGS,
            )
    elif m.text == AnalyticsDetailOptions.DETAILED.value:
        bot.send_message(
            m.chat.id,
            reply_markup=analytics_details_keyboard(),
            text="Now, please, select the category",
            **DEFAULT_SEND_SETTINGS,
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=m.chat.id,
            callback=detailed_option_dispatcher,
            month=month,
        )


@user_error_handler
@restart_handler
def by_month_callback(m: types.Message):
    try:
        datetime.strptime(m.text or "", "%Y-%m")
    except ValueError:
        raise AnalyticsError(f"Date <b>{m.text}</b> doesn't match format YEAR-MONTH")

    bot.send_message(
        m.chat.id,
        reply_markup=analytics_dates_detail_keyboard(),
        text="Select detail level:",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=monthly_dispatcher,
        month=m.text,
    )


@user_error_handler
@restart_handler
def by_year_callback(m: types.Message):
    if not m.text:
        raise AnalyticsError("Year is not selected")

    text = AnalitycsService.get_annyally_report(m.text)

    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=text,
        **DEFAULT_SEND_SETTINGS,
    )


@user_error_handler
@restart_handler
def analytics_dispatcher(m: types.Message):
    if m.text not in AnalyticsOptions.values():
        raise AnalyticsError()

    callback = None
    keyboard = None
    option = None

    if m.text == AnalyticsOptions.BY_MONTH.value:
        option = AnalyticsOptions.BY_MONTH.value
        callback = by_month_callback
        keyboard = exist_dates_keyboard()
    elif m.text == AnalyticsOptions.BY_YEAR.value:
        option = AnalyticsOptions.BY_YEAR.value
        callback = by_year_callback
        keyboard = exist_dates_keyboard(date_format="%Y")

    if not all((callback, keyboard, option)):
        raise AnalyticsError("Keyboard or callback not found")

    bot.send_message(
        m.chat.id,
        reply_markup=keyboard,
        text=f"Use option {option}\nNow, please, select the date 📅",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=callback or (lambda _: None),
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.ANALYTICS.value}")
@user_error_handler
@restart_handler
@only_for_members
def analytics(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=analytics_keyboard(),
        text="Choose option",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=analytics_dispatcher,
    )
