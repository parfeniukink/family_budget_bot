from os import getenv

from telebot import TeleBot

from db import Database, DatabasesService

##############################################
# Database
##############################################
database_service = DatabasesService(
    connection_url=getenv("DATABASE_URL", default="invalid"),
)
database: Database = database_service.get_database()


##############################################
# Bot
##############################################
API_KEY = getenv("API_KEY", default="invalid")
DEFAULT_SEND_SETTINGS = {"disable_web_page_preview": True, "parse_mode": "HTML"}

bot = TeleBot(API_KEY)
