from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import lexicon


def admin_menu(lang: str) -> InlineKeyboardMarkup:
    buttons = ['keygen', 'exit']
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for button in buttons:
        kb_builder.row(InlineKeyboardButton(
            text=lexicon(lang, button),
            callback_data=button))
    return kb_builder.as_markup()
