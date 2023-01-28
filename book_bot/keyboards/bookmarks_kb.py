from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from book_bot.vocabularies.vocab import TEXTS
from book_bot.services.file_handling import book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    bookmarks_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    for btn in sorted(args):
        bookmarks_kb.add(
            InlineKeyboardButton(
                text=f'{btn} - {book[btn][:100]}',
                callback_data=str(btn)
            )
        )
    bookmarks_kb.add(
        InlineKeyboardButton(
            text=TEXTS['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=TEXTS['cancel'],
            callback_data='cancel'
        )
    )
    return bookmarks_kb


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    bookmarks_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()

    for btn in sorted(args):
        bookmarks_kb.add(
            InlineKeyboardButton(
                text=f'{TEXTS["del"]} {btn} - {book[btn][:100]}',
                callback_data=f'{btn}del'
            )
        )
    bookmarks_kb.add(
        InlineKeyboardButton(
            text=TEXTS['cancel'],
            callback_data='cancel'
        )
    )
    return bookmarks_kb
