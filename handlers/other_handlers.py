from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import lexicon

router: Router = Router(name="other-handlers-router")


@router.message()
async def send_echo(message: Message):
    await message.answer(lexicon(lang=message.from_user.language_code, key='reply'))
