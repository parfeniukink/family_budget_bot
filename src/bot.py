from typing import Optional

from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.storage.memory_storage import StateMemoryStorage

from env import Env
from settings import DEFAULT_SEND_SETTINGS

API_KEY = Env.str("API_KEY", default="invalid")
TELEGRAM_MESSAGE_MAX_LEN = 4096

bot = AsyncTeleBot(API_KEY, state_storage=StateMemoryStorage())


class CallbackMessages:
    @staticmethod
    async def edit(
        q: types.CallbackQuery, text: str, reply_markup: Optional[types.InlineKeyboardMarkup] = None
    ) -> None:
        extra_payload = {}

        if reply_markup:
            extra_payload["reply_markup"] = reply_markup

        await bot.edit_message_text(
            chat_id=q.message.chat.id,
            message_id=q.message.id,
            text=text,
            **DEFAULT_SEND_SETTINGS,
            **extra_payload,
        )

    @staticmethod
    async def delete(q: types.CallbackQuery) -> None:
        await bot.delete_message(chat_id=q.message.chat.id, message_id=q.message.id)
