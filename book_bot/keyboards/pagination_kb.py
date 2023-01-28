from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from book_bot.vocabularies.vocab import TEXTS


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    pagination_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    pagination_kb.row(*[
        InlineKeyboardButton(TEXTS.get(btn, btn), callback_data=btn)
        for btn in buttons
    ])
    return pagination_kb
