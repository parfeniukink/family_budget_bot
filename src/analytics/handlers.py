from telebot import types

from analytics.errors import AnalyticsError
from analytics.keyboards import (
    AnalyticsDetailOptions,
    AnalyticsOptions,
    analytics_dates_detail_keyboard,
    analytics_dates_keyboard,
    analytics_keyboard,
)
from analytics.services import AnalitycsService
from config import DEFAULT_SEND_SETTINGS, bot
from keyboards import default_keyboard
from shared.analytics import KeyboardButtons
from shared.errors import user_error_handler


@user_error_handler
def monthly_dispatcher(m: types.Message, month: str):
    if m.text not in AnalyticsDetailOptions.values():
        raise AnalyticsError()

    report = ""

    if m.text == AnalyticsDetailOptions.BASIC.value:
        report = AnalitycsService.get_monthly_basic_report(month)
    elif m.text == AnalyticsDetailOptions.DETAILED.value:
        report = AnalitycsService.get_monthly_detailed_report(month)

    if len(report) > 4000:
        bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text="Only basic report is allowed",
            **DEFAULT_SEND_SETTINGS,
        )

    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=report,
        **DEFAULT_SEND_SETTINGS,
    )


@user_error_handler
def by_date_callback(m: types.Message):
    if not m.text:
        raise AnalyticsError("Date is not selected")

    bot.send_message(
        m.chat.id,
        reply_markup=analytics_dates_detail_keyboard(),
        text="Select detail option",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=monthly_dispatcher,
        month=m.text,
    )


@user_error_handler
def analytics_dispatcher(m: types.Message):
    if m.text not in AnalyticsOptions.values():
        raise AnalyticsError()

    callback = None

    if m.text == AnalyticsOptions.BY_MONTH.value:
        callback = by_date_callback

    bot.send_message(
        m.chat.id,
        reply_markup=analytics_dates_keyboard(),
        text=f"Use option {AnalyticsOptions.BY_MONTH.name}",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=callback or (lambda _: None),
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.ANALYTICS.value}")
@user_error_handler
def add_costs(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=analytics_keyboard(),
        text="Choose option",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=analytics_dispatcher,
    )
