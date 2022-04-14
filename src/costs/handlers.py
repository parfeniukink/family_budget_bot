from telebot import types

from config import bot
from keyboards import default_keyboard


@bot.message_handler(regexp=r"Add cost")
def add_costs(m: types.Message):
    bot.send_message(m.chat.id, reply_markup=default_keyboard(), text="Let's add some costs")
