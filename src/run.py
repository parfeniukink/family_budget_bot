from time import sleep

from loguru import logger

from analytics.handlers import *  # noqa
from bot import bot
from configurations.handlers import *  # noqa
from costs.handlers import *  # noqa
from equity.handlers import *  # noqa
from incomes.handlers import *  # noqa
from startup.handlers import *  # noqa


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
