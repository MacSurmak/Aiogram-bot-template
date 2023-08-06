from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

router: Router = Router(name="other-handlers-router")


@router.message()
async def send_echo(message: Message):
    await message.answer(LEXICON_RU['reply'])
