from bot import bot
from shared.domain import base_error_handler
from storages import State


@bot.message_handler(func=lambda _: True)
@base_error_handler
async def all_messages(m):
    state = State(m.from_user.id)

    if not state.storage or not state.key or not state.callback:
        return await bot.send_message(m.chat.id, "Please use keyboard")

    if state.validator:
        state.validator(m.text)

    setattr(state.storage, state.key, m.text)
    next_callback = state.callback
    state.clean()

    return await next_callback(m)
