from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from database.models import User
from filters import IsAdmin

router: Router = Router(name='commands-router')


@router.message(CommandStart(), IsAdmin())
async def process_start_command_admin(message: Message, session: AsyncSession):
    """
    Handles /start command and adds user into database
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    """
    await message.answer(LEXICON_RU['/start-admin'])
    await session.merge(User(user_id=message.from_user.id))
    await session.commit()


@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    """
    Handles /start command and adds user into database
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    """
    await message.answer(LEXICON_RU['/start'])
    await session.merge(User(user_id=message.from_user.id))
    await session.commit()


@router.message(Command("help"))
async def process_start_command(message: Message):
    """
    Handles /help command
    :param message: Telegram message with "/start" text
    """
    await message.answer(LEXICON_RU['/help'])
