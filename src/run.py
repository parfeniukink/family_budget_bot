import asyncio
import warnings
from time import sleep

from loguru import logger

from analytics.handlers import *  # noqa
from bot import bot
from configurations.handlers import *  # noqa
from costs.handlers import *  # noqa
from equity.handlers import *  # noqa
from incomes.handlers import *  # noqa
from shared.handlers import *  # noqa

warnings.filterwarnings("ignore", category=DeprecationWarning)

logger.add("fbb.log", rotation="50 MB")


async def start_bot():
    try:
        logger.info("Bot started 🚀")
        await bot.polling(none_stop=True, interval=0)
    except Exception as err:
        logger.error(err)
        logger.error("🔴 Bot is down.\nRestarting...")
        logger.info("Sleeping for 30 seconds")
        sleep(5)
        await start_bot()


async def integrations_background():
    while True:
        await asyncio.sleep(300)
        logger.debug("Integrations engine")


loop = asyncio.get_event_loop()
tasks = [start_bot(), integrations_background()]
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()
