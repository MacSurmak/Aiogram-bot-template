from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter, Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import lexicon
from filters.filters import IsRegistered, IsAdmin
from keyboards.admin import admin_cancel, admin_menu
from services.remove_old_markups import save_markups, remove_old_markups

router: Router = Router(name="admin-handlers-router")
router.callback_query.filter(IsAdmin())
router.message.filter(IsAdmin())


class FSMKeygen(StatesGroup):
    fill_room = State()
    fill_surname = State()
    fill_name = State()


@router.message(Command("admin"))
async def process_admin_command(message: Message, lang: str, state: FSMContext):
    """
    Handles /admin command if user is in admin list and
    replies with an admin markup
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    await remove_old_markups(state)
    await state.clear()
    msg = await message.answer(text=lexicon(lang, '/admin'),
                               reply_markup=admin_menu(lang))
    await save_markups(msg, state)


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
    msg = await callback.message.edit_text(text=lexicon(lang, 'enter-room'),
                                           reply_markup=admin_cancel(lang))
    await state.set_state(FSMKeygen.fill_room)
    await save_markups(msg, state)


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
        msg = await message.answer(text=lexicon(lang, 'enter-surname'),
                                   reply_markup=admin_cancel(lang))
        await state.set_state(FSMKeygen.fill_surname)
        await state.update_data(room=int(message.text))
    else:
        msg = await message.answer(text=lexicon(lang, 'wrong-number'),
                                   reply_markup=admin_cancel(lang))
    await remove_old_markups(msg, state)


@router.message(StateFilter(FSMKeygen.fill_room))
async def process_room_wrong(message: Message, lang: str, state: FSMContext):
    """
    Handles room number
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    msg = await message.answer(text=lexicon(lang, 'room-not-digit'),
                               reply_markup=admin_cancel(lang))
    await remove_old_markups(msg, state)


@router.message(StateFilter(FSMKeygen.fill_surname), F.text.isalpha())
async def process_surname(message: Message, lang: str, state: FSMContext):
    """
    Handles surname
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    msg = await message.answer(text=lexicon(lang, 'enter-name'),
                               reply_markup=admin_cancel(lang))
    await state.set_state(FSMKeygen.fill_name)
    await state.update_data(surname=(message.text[0].upper() + message.text[1:].lower()))
    await remove_old_markups(msg, state)


@router.message(StateFilter(FSMKeygen.fill_surname))
async def process_surname_wrong(message: Message, lang: str, state: FSMContext):
    """
    Handles surname
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    msg = await message.answer(text=lexicon(lang, 'surname-wrong'),
                               reply_markup=admin_cancel(lang))
    await remove_old_markups(msg, state)


@router.message(StateFilter(FSMKeygen.fill_name), F.text.isalpha())
async def process_name(message: Message, lang: str, state: FSMContext):
    """
    Handles name
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    await state.update_data(name=(message.text[0].upper() + message.text[1:].lower()))
    data = await state.get_data()
    msg = await message.answer(text=lexicon(lang, 'keygen-checkup').format(data['surname'],
                                                                           data['name'],
                                                                           data['room']),
                               reply_markup=admin_cancel(lang, lexicon(lang, '_yes')))
    await remove_old_markups(msg, state)


@router.message(StateFilter(FSMKeygen.fill_name))
async def process_name_wrong(message: Message, lang: str, state: FSMContext):
    """
    Handles name
    :param message: Telegram message
    :param lang: user's language code
    :param state: FSM state
    """
    msg = await message.answer(text=lexicon(lang, 'name-wrong'),
                               reply_markup=admin_cancel(lang))
    await remove_old_markups(msg, state)


@router.callback_query(lambda callback: callback.data == '_yes', StateFilter(FSMKeygen.fill_name))
async def create_key(callback: CallbackQuery, lang: str, state: FSMContext):
    """
    Creates and sends key
    :param callback: Telegram callback
    :param lang: user's language code
    :param state: FSM state
    """
    data = await state.get_data()
    await state.clear()
    await callback.message.edit_text(text=lexicon(lang, 'keygen-done'),
                                     reply_markup=None)
    key = f"<tg-spoiler>{data['surname']}-{data['room']}</tg-spoiler>"
    await callback.message.answer(key)
    msg = await callback.message.answer(text=lexicon(lang, '/admin'),
                                        reply_markup=admin_menu(lang))
    await remove_old_markups(msg, state, remove=False)
