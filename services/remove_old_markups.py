from aiogram.exceptions import TelegramBadRequest

from database import save_message_id, get_message_id


async def remove_old_markups(session, bot, message, new_message):
    old_msg = await get_message_id(session, message.from_user.id)
    try:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=old_msg, reply_markup=None)
    except TelegramBadRequest:
        pass
    await save_message_id(session, message.from_user.id, new_message.message_id)
