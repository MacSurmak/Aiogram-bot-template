from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import lexicon
from database import User, add_user, get_id
from filters.filters import IsRegistered

router: Router = Router(name='commands-router')


@router.message(CommandStart(), ~IsRegistered())
async def process_start_command(message: Message, session: AsyncSession, lang: str):
    """
    Handles /start command and adds user into database
    :param message: Telegram message
    :param session: DB connection session
    :param lang: user's language code
    """
    await get_id(session=session)
    await message.answer(text=lexicon(lang, '/start'))
    await add_user(session,
                   user_id=message.from_user.id,
                   username=message.from_user.username,
                   name=f"{message.from_user.first_name} {message.from_user.last_name}")


@router.message(CommandStart())
async def process_start_command_registered(message: Message, lang: str):
    """
    Handles /start command if user is already registered
    :param message: Telegram message
    :param lang: user's language code
    """
    await message.answer(text=lexicon(lang, '/start-registered'))


@router.message(Command("help"))
async def process_help_command(message: Message, lang: str):
    """
    Handles /help command
    :param message: Telegram message
    :param lang: user's language code
    """
    await message.answer(text=lexicon(lang, '/help'))


# @router.message(Command("list"))
# async def get_user_list(message: Message, session: AsyncSession, lang: str):
#     """
#     Handles /start command and adds user into database
#     :param message: Telegram message
#     :param session: DB connection session
#     :param lang: user's language code
#     """
#     await get_id(session=session)
