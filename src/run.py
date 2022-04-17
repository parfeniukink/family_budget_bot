from loguru import logger

from analytics.handlers import *  # noqa
from config import bot, database
from configurations.handlers import *  # noqa
from costs.handlers import *  # noqa
from equity.handlers import *  # noqa
from handlers import *  # noqa
from incomes.handlers import *  # noqa

# Init database
database.init()

# Start bot
logger.info("Bot started 🚀")
bot.polling(none_stop=True, interval=0)
