from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter, or_f
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import lexicon
from filters.filters import IsRegistered, IsAdmin
from keyboards.admin import admin_cancel, admin_menu

router: Router = Router(name="admin-handlers-router")
router.callback_query.filter(IsAdmin())
router.message.filter(IsAdmin())


class FSMKeygen(StatesGroup):
    fill_room = State()
    fill_surname = State()
    fill_name = State()


@router.callback_query(lambda callback: callback.data == '_exit')
async def admin_exit(callback: CallbackQuery, lang: str):
    """
    Handles callback with 'exit' and returns admin into
    user menu
    :param callback: Telegram callback
    :param lang: user's language code
    """
    await callback.message.edit_text(text=lexicon(lang, 'user-back'),
                                     reply_markup=None)


@router.callback_query(lambda callback: callback.data == '_keygen')
async def admin_keygen(callback: CallbackQuery, lang: str, state: FSMContext):
    """
    Forces admin into keygen scenario
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    await callback.message.edit_text(text=lexicon(lang, 'enter-room'),
                                     reply_markup=admin_cancel(lang))
    await state.set_state(FSMKeygen.fill_room)


@router.callback_query(lambda callback: callback.data == '_cancel',
                       StateFilter(FSMKeygen.fill_room,
                                   FSMKeygen.fill_name,
                                   FSMKeygen.fill_surname))
async def admin_cancel_keygen(callback: CallbackQuery, lang: str, state: FSMContext):
    """
    Cancels admin keygen scenario
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    await callback.message.edit_text(text=lexicon(lang, '/admin'),
                                     reply_markup=admin_menu(lang))
    await state.clear()


@router.message(StateFilter(FSMKeygen.fill_room), F.text.isdigit())
async def process_room(message: Message, lang: str, state: FSMContext):
    """
    Handles room number
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    if 500 > int(message.text) > 200:
        await message.answer(lexicon(lang, 'enter-surname'))
        await state.set_state(FSMKeygen.fill_surname)
    else:
        await message.answer(lexicon(lang, 'wrong-number'))


@router.message(StateFilter(FSMKeygen.fill_room))
async def process_room_wrong(message: Message, lang: str, state: FSMContext):
    """
    Handles room number
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    await message.answer(lexicon(lang, 'room-not-digit'))
