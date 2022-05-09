from telebot import types

from bot import bot
from equity.domain import EquityGeneralMenu
from equity.services import EquityCRUD
from shared.domain import base_error_handler, restart_handler
from shared.keyboards import default_keyboard
from users import UsersService


@bot.message_handler(regexp=rf"^{EquityGeneralMenu.EQUITY.value}")
@restart_handler
@base_error_handler
@UsersService.only_for_members
async def equity(m: types.Message):
    text = EquityCRUD.get_formatted()
    await bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=text,
    )
