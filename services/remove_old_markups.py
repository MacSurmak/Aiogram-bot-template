from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def save_markups(msg: Message, state: FSMContext):
    await state.update_data(old_message_id=msg.message_id,
                            old_chat_id=msg.chat.id)


async def remove_old_markups(state: FSMContext):
    data = await state.get_data()
    await state.bot.edit_message_reply_markup(message_id=data['old_message_id'],
                                              chat_id=data['old_chat_id'],
                                              reply_markup=None)
