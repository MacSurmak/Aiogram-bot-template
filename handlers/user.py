from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import lexicon

router: Router = Router(name="user-handlers-router")


@router.message()
async def send_echo(message: Message, lang: str):
    """
    Handles any other text and replies with something
    :param message: Telegram message
    :param lang: user's language code
    """
    await message.answer(text=lexicon(lang, 'reply-other'))
