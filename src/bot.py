from telebot import TeleBot

from env import Env

API_KEY = Env.str("API_KEY", default="invalid")
TELEGRAM_MESSAGE_MAX_LEN = 4096

bot = TeleBot(API_KEY)
