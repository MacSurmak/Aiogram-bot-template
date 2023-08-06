from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import lexicon
from database import User, add_user
from filters.filters import IsRegistered, IsAdmin

router: Router = Router(name='commands-router')


@router.message(CommandStart(), ~IsRegistered())
async def process_start_command(message: Message, session: AsyncSession):
    """
    Handles /start command and adds user into database
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    """
    await message.answer(lexicon(lang=message.from_user.language_code, key='/start'))
    await add_user(session, message.from_user.id)


@router.message(CommandStart(), IsAdmin())
async def process_start_command_admin(message: Message, session: AsyncSession):
    """
    Handles /start command
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    """
    await message.answer(lexicon(lang=message.from_user.language_code, key='/start-admin'))


@router.message(CommandStart(), IsRegistered())
async def process_start_command_registered(message: Message, session: AsyncSession):
    """
    Handles /start command
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    """
    await message.answer(lexicon(lang=message.from_user.language_code, key='/start-registered'))


@router.message(Command("help"))
async def process_start_command(message: Message):
    """
    Handles /help command
    :param message: Telegram message with "/start" text
    """
    await message.answer(lexicon(lang=message.from_user.language_code, key='/help'))
