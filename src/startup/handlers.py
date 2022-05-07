from loguru import logger
from telebot import types

from bot import bot
from settings import DEFAULT_SEND_SETTINGS
from shared.domain import base_error_handler
from shared.keyboards import default_keyboard
from shared.messages import LINE_ITEM, RESTART
from startup.messages import USER_CREATED_MESSAGE, USER_EXISTS_MESSAGE
from users import UsersCRUD, UsersService


@bot.message_handler(commands=["start"])
@base_error_handler
@UsersService.only_for_members
async def start(m: types.Message):
    user, created = UsersCRUD.save_user(m)
    if created:
        logger.success(LINE_ITEM.format(key="Created a new user", value=user.username))
        await bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=USER_CREATED_MESSAGE,
            **DEFAULT_SEND_SETTINGS,
        )
    else:
        logger.info(LINE_ITEM.format(key="User exists", value=user.username))
        await bot.send_message(
            m.chat.id,
            reply_markup=default_keyboard(),
            text=USER_EXISTS_MESSAGE,
            **DEFAULT_SEND_SETTINGS,
        )


@bot.message_handler(commands=["restart"])
@base_error_handler
@UsersService.only_for_members
async def restart(m: types.Message):
    await bot.send_message(
        m.chat.id,
        reply_markup=default_keyboard(),
        text=RESTART,
        **DEFAULT_SEND_SETTINGS,
    )


# @bot.inline_handler(lambda query: query.query == "test_message")
# async def test_message(inline):
#     logger.debug("test 1")


# @bot.inline_handler(lambda query: query.query == "test2_message")
# async def test2_message(inline):
#     logger.debug("test 2")


# def uuid_facory():
#     items = set()

#     while True:
#         item = str(uuid4())
#         if item not in items:
#             items.add(item)
#             yield item
#         else:
#             continue


# random_uuid: Iterator = uuid_facory()


# class Tests(Enum):
#     test_1 = next(random_uuid)
#     test_2 = next(random_uuid)
#     test_3 = next(random_uuid)


# def inline_keyboard():
#     return types.InlineKeyboardMarkup(
#         keyboard=[
#             [
#                 types.InlineKeyboardButton(text=Tests.test_1.name, callback_data=Tests.test_1.value),
#                 types.InlineKeyboardButton(text=Tests.test_2.name, callback_data=Tests.test_2.value),
#             ],
#             [
#                 types.InlineKeyboardButton(text=Tests.test_3.name, callback_data=Tests.test_3.value),
#             ],
#         ]
#     )


# @bot.callback_query_handler(lambda x: True)
# async def foo(call):
#     logger.debug("Foo called")
#     logger.debug(call.data)


# @bot.message_handler(commands=["help"])
# async def help(m: types.Message):
#     await bot.send_message(
#         m.chat.id,
#         reply_markup=inline_keyboard(),
#         text=RESTART,
#         **DEFAULT_SEND_SETTINGS,
#     )
