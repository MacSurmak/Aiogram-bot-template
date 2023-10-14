from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import lexicon
from handlers.FSM_classes import FSMSubscription
from database import update_subscription_status

router: Router = Router(name="user-handlers-router")


@router.callback_query(lambda callback: callback.data == '_yes', StateFilter(FSMSubscription.subscribe))
async def subscribe_yes(callback: CallbackQuery, session: AsyncSession, lang: str, state: FSMContext):
    """
    Handles callback
    :param session: DB connection session
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    await update_subscription_status(session, callback.from_user.id, True)
    await callback.message.edit_text(text=lexicon(lang, 'subscribe-yes'),
                                     reply_markup=None)
    await state.clear()


@router.callback_query(lambda callback: callback.data == '_no', StateFilter(FSMSubscription.subscribe))
async def subscribe_no(callback: CallbackQuery, session: AsyncSession, lang: str, state: FSMContext):
    """
    Handles callback
    :param session: DB connection session
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    await callback.message.edit_text(text=lexicon(lang, 'subscribe-no'),
                                     reply_markup=None)
    await state.clear()


@router.callback_query(lambda callback: callback.data == '_yes', StateFilter(FSMSubscription.unsubscribe))
async def unsubscribe_yes(callback: CallbackQuery, session: AsyncSession, lang: str, state: FSMContext):
    """
    Handles callback
    :param session: DB connection session
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    await update_subscription_status(session, callback.from_user.id, False)
    await callback.message.edit_text(text=lexicon(lang, 'unsubscribe-yes'),
                                     reply_markup=None)
    await state.clear()


@router.callback_query(lambda callback: callback.data == '_no', StateFilter(FSMSubscription.unsubscribe))
async def unsubscribe_no(callback: CallbackQuery, lang: str, state: FSMContext):
    """
    Handles callback
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    await callback.message.edit_text(text=lexicon(lang, 'unsubscribe-no'),
                                     reply_markup=None)
    await state.clear()


@router.message()
async def send_echo(message: Message, lang: str):
    """
    Handles any other text and replies with something
    :param message: Telegram message
    :param lang: user's language code
    """
    await message.answer(text=lexicon(lang, 'reply-other'))
