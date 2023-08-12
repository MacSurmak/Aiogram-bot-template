from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import lexicon
from database import User, add_user
from filters.filters import IsRegistered, IsAdmin
from keyboards.test import create_keyboard

router: Router = Router(name='commands-router')


@router.message(CommandStart(), ~IsRegistered())
async def process_start_command(message: Message, session: AsyncSession, lang: str):
    """
    Handles /start command and adds user into database
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    :param lang: user's language code
    """
    await message.answer(lexicon(lang, '/start'))
    await add_user(session, message.from_user.id)


@router.message(CommandStart(), IsAdmin())
async def process_start_command_admin(message: Message, session: AsyncSession, lang: str):
    """
    Handles /start command
    :param message: Telegram message with "/start" text
    :param session: DB connection session
    :param lang: user's language code
    """
    await message.answer(text=lexicon(
                            lang=message.from_user.language_code,
                            key='/start-admin'),
                         reply_markup=create_keyboard(
                             2,
                             lang,
                             'reply'))


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


@router.callback_query()
async def process_inline(callback: CallbackQuery, session: AsyncSession, lang: str):
    """
    Handles inline updates
    :param callback: Telegram message with "/start" text
    :param session: DB connection session
    :param lang: user's language code
    """
    await callback.message.answer(text=lang)
