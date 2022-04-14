from loguru import logger

from config import bot, database
from costs.handlers import *  # noqa
from handlers import *  # noqa

# Init database
database.init()

# Start bot
logger.info("Bot started 🚀")
bot.polling(none_stop=True, interval=0)
