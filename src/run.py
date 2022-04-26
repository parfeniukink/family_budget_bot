from time import sleep

from loguru import logger

from config import bot, database
from handlers import *  # noqa

# NOTE: Init database
database.init()


# NOTE: Start bot
def start_bot():
    try:
        logger.info("Bot started 🚀")
        bot.polling(none_stop=True, interval=0)
    except Exception as err:
        logger.error(err)
        logger.error("🔴 Bot is down.\nRestarting...")
        logger.info("Sleeping for 30 seconds")
        sleep(30)
        start_bot()


start_bot()
