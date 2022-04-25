from telebot import types

from config import DEFAULT_SEND_SETTINGS, bot
from costs.errors import CostsError
from costs.keyboards import categories_keyboard, ids_keyboard
from costs.models import Cost
from costs.services import CostsService
from keyboards import confirmation_keyboard, dates_keyboard, default_keyboard
from shared.categories import CATEGORIES_EMOJI
from shared.costs import KeyboardButtons
from shared.dates import exist_dates_keyboard
from shared.errors import user_error_handler
from shared.handlers import restart_handler


#####################################################
# Add costs
#####################################################
@user_error_handler
@restart_handler
def confirmation(m: types.Message, costs_service: CostsService):
    processed: bool = costs_service.process_confirmation(m.text)
    message = "✅ Costs saved" if processed else "❌ Costs wasn't added"

    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text=message)


@user_error_handler
@restart_handler
def add_value(m: types.Message, costs_service: CostsService):
    costs_service.add_value(m.text)
    category = costs_service._category.name if costs_service._category else ""
    category_emoji = CATEGORIES_EMOJI.get(category, "")
    date = costs_service._date.strftime("%m-%d") if costs_service._date else ""
    next_step_text = "\n".join(
        [
            "Would you like to save this costs ❓\n",
            f"Date 👉 {date}",  # type: ignore
            f"Category 👉 {category} {category_emoji}",  # type: ignore
            f"Description 👉 {costs_service._text}",
            f"Value 👉 {costs_service._value}",
        ]
    )
    bot.send_message(
        m.chat.id,
        reply_markup=confirmation_keyboard(),
        text=next_step_text,
        **DEFAULT_SEND_SETTINGS,
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=confirmation,
        costs_service=costs_service,
    )


@user_error_handler
@restart_handler
def add_text(m: types.Message, costs_service: CostsService):
    costs_service.add_text(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=f"✅ Description added 👉 {m.text}\nNow, please, enter the value",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=add_value,
        costs_service=costs_service,
    )


@user_error_handler
@restart_handler
def select_date(m: types.Message, costs_service: CostsService):
    costs_service.set_date(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=types.ReplyKeyboardRemove(),
        text=f"✅ Date selected 👉 {m.text}\nNow, please, enter the description",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=add_text,
        costs_service=costs_service,
    )


@user_error_handler
@restart_handler
def select_category(m: types.Message, costs_service: CostsService):
    costs_service.set_category(m.text)
    bot.send_message(
        m.chat.id,
        reply_markup=dates_keyboard(),
        text=f"✅ Category 👉 {m.text} selected\nNow, please, select the date 📅 from the list",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_date,
        costs_service=costs_service,
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.ADD_COST.value}")
@user_error_handler
@restart_handler
def add_costs(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=categories_keyboard(),
        text="Please, select category from the list",
    )
    costs_service = CostsService(account_id=m.from_user.id)

    bot.register_next_step_handler_by_chat_id(chat_id=m.chat.id, callback=select_category, costs_service=costs_service)


#####################################################
# Delete costs
#####################################################
@user_error_handler
@restart_handler
def select_id_for_delete(m: types.Message, service: CostsService, allowed_ids: set):
    if m.text not in allowed_ids:
        raise CostsError(f"⚠️ Can not find id 👉 {m.text}\nPlease use the keyboard below!")

    service.delete_by_id(m.text)
    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text="✅ Cost removed")


@user_error_handler
@restart_handler
def select_category_for_delete(m: types.Message, service: CostsService, costs: list[Cost]):
    service.set_category(m.text)
    filtered_costs = [cost for cost in costs if cost.category_id == service._category.id]  # type: ignore
    f_costs = service.get_formatted_costs_for_delete(filtered_costs)

    bot.send_message(
        m.chat.id,
        reply_markup=ids_keyboard(reversed(filtered_costs)),
        text=f"✅ Category selected 👉 {m.text}\nNow, please, select the id to delete\n{f_costs}",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_id_for_delete,
        service=service,
        allowed_ids={cost.id for cost in filtered_costs},
    )


@user_error_handler
@restart_handler
def select_month_for_delete(m: types.Message, service: CostsService):
    if not m.text:
        raise CostsError("⚠️ No month selected")

    costs: dict[str, list[Cost]] = service.get_monthly_costs(m.text)
    merged_costs = [el for key in costs for el in costs[key]]

    bot.send_message(
        m.chat.id,
        reply_markup=categories_keyboard(),
        text=f"✅ Date selected 👉 {m.text}\nNow, please, select category",
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_category_for_delete,
        service=service,
        costs=merged_costs,
    )


@bot.message_handler(regexp=rf"^{KeyboardButtons.DELETE_COST.value}")
@user_error_handler
@restart_handler
def delete_costs(m: types.Message):
    bot.send_message(
        m.chat.id,
        reply_markup=exist_dates_keyboard(),
        text="Please, select month from the list",
    )
    service = CostsService(account_id=m.from_user.id)

    bot.register_next_step_handler_by_chat_id(
        chat_id=m.chat.id,
        callback=select_month_for_delete,
        service=service,
    )
