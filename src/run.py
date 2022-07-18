import asyncio
from time import sleep

from loguru import logger

from analytics.handlers import *  # noqa
from bot import bot
from configurations.handlers import *  # noqa
from costs.handlers import *  # noqa
from equity.handlers import *  # noqa
from incomes.handlers import *  # noqa
from shared.handlers import *  # noqa

logger.add("fbb.log", rotation="50 MB")


async def start_bot():
    try:
        logger.info("Bot started 🚀")
        await bot.polling(none_stop=True, interval=0)
    except Exception as err:
        logger.error(err)
        logger.error("🔴 Bot is down.\nRestarting...")
        logger.info("🕟 Sleeping for 5 seconds")
        sleep(5)
        await start_bot()


# NOTE: Template for future background integration workers
async def integrations_background():
    logger.debug("Integrations engine")


async def main():
    tasks = [start_bot(), integrations_background()]
    await asyncio.gather(*tasks)


# NOTE: Run the application
asyncio.run(main())
