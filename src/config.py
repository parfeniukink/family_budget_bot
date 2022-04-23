from os import getenv

from telebot import TeleBot, types

from db import Database, DatabasesService

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

DEFAULT_SEND_SETTINGS = {"disable_web_page_preview": True, "parse_mode": "HTML"}

HELP_TEXT = "/restart"
HELP_BUTTON = types.KeyboardButton(HELP_TEXT)

DATES_KEYBOARD_LEN: int = int(getenv("DATES_KEYBOARD_LEN", default=10))

bot = TeleBot(API_KEY)
