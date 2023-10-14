from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import lexicon
from database import add_user, get_id
from filters.filters import IsRegistered
from keyboards.user import yes_no
from handlers.FSM_classes import FSMSubscription
from services.remove_old_markups import remove_old_markups

router: Router = Router(name='commands-router')


@router.message(CommandStart(), ~IsRegistered())
async def process_start_command(message: Message, session: AsyncSession, lang: str, state: FSMContext, bot: Bot):
    """
    Handles /start command and adds user into database
    :param message: Telegram message
    :param session: DB connection session
    :param lang: user's language code
    :param state: FSM state
    :param bot: Bot instance
    """
    msg = await message.answer(text=lexicon(lang, '/start'),
                               reply_markup=yes_no(lang))
    await state.set_state(FSMSubscription.subscribe)
    await add_user(session,
                   user_id=message.from_user.id,
                   username=message.from_user.username,
                   name=f"{message.from_user.first_name} {message.from_user.last_name}")

    await remove_old_markups(session, bot, message, msg)


@router.message(CommandStart(), StateFilter(FSMSubscription.subscribe,
                                            FSMSubscription.unsubscribe))
async def process_start_subscribe(message: Message, session: AsyncSession, lang: str, state: FSMContext, bot: Bot):
    """
    Handles /start command when waiting for subscription confirmation
    :param message: Telegram message
    :param session: DB connection session
    :param lang: user's language code
    :param state: FSM state
    :param bot: Bot instance
    """
    msg = await message.answer(text=lexicon(lang, '/start-subscribe'),
                               reply_markup=yes_no(lang))

    await remove_old_markups(session, bot, message, msg)


@router.message(CommandStart())
async def process_start_command_registered(message: Message, lang: str, bot: Bot, session: AsyncSession):
    """
    Handles /start command if user is already registered
    :param message: Telegram message
    :param lang: user's language code
    :param bot: Bot instance
    :param session: DB connection session
    """
    msg = await message.answer(text=lexicon(lang, '/start-registered'))

    await remove_old_markups(session, bot, message, msg)


@router.message(Command("help"))
async def process_help_command(message: Message, lang: str):
    """
    Handles /help command
    :param message: Telegram message
    :param lang: user's language code
    """
    await message.answer(text=lexicon(lang, '/help'))


@router.message(Command("subscribe"))
async def process_unsubscribe_command(message: Message, session: AsyncSession, lang: str, state: FSMContext, bot: Bot):
    """
    Handles /subscribe command
    :param message: Telegram message
    :param session: DB connection session
    :param lang: user's language code
    :param state: FSM state
    :param bot: Bot instance
    """
    await state.set_state(FSMSubscription.subscribe)

    subscribed = await get_id(session)

    if message.from_user.id not in subscribed:
        msg = await message.answer(text=lexicon(lang, '/subscribe'),
                                   reply_markup=yes_no(lang))
    else:
        msg = await message.answer(text=lexicon(lang, 'already-subscribed'))

    await remove_old_markups(session, bot, message, msg)


@router.message(Command("unsubscribe"))
async def process_unsubscribe_command(message: Message, session: AsyncSession, lang: str, state: FSMContext, bot: Bot):
    """
    Handles /unsubscribe command
    :param message: Telegram message
    :param session: DB connection session
    :param lang: user's language code
    :param state: FSM state
    :param bot: Bot instance
    """
    await state.set_state(FSMSubscription.unsubscribe)

    subscribed = await get_id(session)

    if message.from_user.id in subscribed:
        msg = await message.answer(text=lexicon(lang, '/unsubscribe'),
                                   reply_markup=yes_no(lang))
    else:
        msg = await message.answer(text=lexicon(lang, 'already-unsubscribed'))

    await remove_old_markups(session, bot, message, msg)
