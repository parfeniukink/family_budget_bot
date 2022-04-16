from telebot import types

from config import bot
from equity.services import EquityService
from keyboards import default_keyboard
from shared.equity import KeyboardButtons


@bot.message_handler(regexp=rf"^{KeyboardButtons.EQUITY.value}")
def configurations(m: types.Message):
    text = EquityService.get_formatted()
    bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=text,
    )
