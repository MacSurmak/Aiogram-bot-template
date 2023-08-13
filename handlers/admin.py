from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F

from lexicon.lexicon import lexicon
from filters.filters import IsRegistered, IsAdmin

router: Router = Router(name="admin-handlers-router")
router.callback_query.filter(IsAdmin())
router.message.filter(IsAdmin())


@router.callback_query(lambda callback: callback.data == 'exit')
async def admin_exit(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(text=lexicon(lang, '/user'),
                                     reply_markup=None)
