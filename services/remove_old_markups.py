from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def remove_old_markups(msg: Message, state: FSMContext):
    data = await state.get_data()
    if 'old_message' in data:
        data['old_message'].edit_text(reply_markup=None)
    await state.update_data(old_message=msg)
