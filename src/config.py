from os import getenv
from typing import Any

from telebot import TeleBot, types

from db import Database, DatabasesService
from shared.env import Env

##############################################
# Database
##############################################
database_service = DatabasesService(
    host=getenv("POSTGRES_HOST"),
    port=int(getenv("POSTGRES_PORT", "5432")),
    username=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
    dbname=getenv("POSTGRES_DB"),
)
database: Database = database_service.get_database()


##############################################
# Bot
##############################################
API_KEY = getenv("API_KEY", default="invalid")
TELEGRAM_MESSAGE_MAX_LEN = 4096

bot = TeleBot(API_KEY)


##############################################
# Application
##############################################
DEFAULT_SEND_SETTINGS: dict[str, Any] = {"disable_web_page_preview": True, "parse_mode": "HTML"}
RESTART_BUTTON_TEXT: str = "/restart"
RESTART_BUTTON: types.KeyboardButton = types.KeyboardButton(RESTART_BUTTON_TEXT)
ALLOWED_USER_ACCOUNT_IDS: list = Env.list(getenv("USERS_ACL", default=""))

DATES_KEYBOARD_LEN: int = int(getenv("DATES_KEYBOARD_LEN", default=10))
