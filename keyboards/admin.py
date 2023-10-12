from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import lexicon


def admin_menu(lang: str) -> InlineKeyboardMarkup:
    buttons = ['_keygen', '_exit']
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for button in buttons:
        kb_builder.row(InlineKeyboardButton(
            text=lexicon(lang, button),
            callback_data=button))
    return kb_builder.as_markup()


def admin_cancel(lang: str, *args) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(InlineKeyboardButton(
            text=lexicon(lang, button),
            callback_data=button))
    kb_builder.row(InlineKeyboardButton(
        text=lexicon(lang, '_cancel'),
        callback_data='_cancel'))
    return kb_builder.as_markup()
