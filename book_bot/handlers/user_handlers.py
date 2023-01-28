from copy import deepcopy

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from book_bot.db.db import user_dict_template, user_db
from book_bot.keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                             create_edit_keyboard)
from book_bot.keyboards.pagination_kb import create_pagination_keyboard
from book_bot.vocabularies.vocab import TEXTS
from book_bot.services.file_handling import book


def _get_page_content(user_id):
    page = user_db[user_id]['page']
    return {
        'text': book[page],
        'reply_markup': create_pagination_keyboard(
            'backward',
            f'{page}/{len(book)}',
            'forward')
    }


async def process_start_command(message: Message):
    await message.answer(TEXTS[message.text])
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)


async def process_help_command(message: Message):
    await message.answer(TEXTS[message.text])


async def process_beginning_command(message: Message):
    user_id = message.from_user.id
    user_db[user_id]['page'] = 1
    await message.answer(**_get_page_content(user_id))


async def process_continue_command(message: Message):
    user_id = message.from_user.id
    await message.answer(**_get_page_content(user_id))


async def process_bookmarks_command(message: Message):
    user_id = message.from_user.id
    if user_db[user_id]['bookmarks']:
        await message.answer(
            text=TEXTS['/bookmarks'],
            reply_markup=create_bookmarks_keyboard(
                *user_db[user_id]['bookmarks']))
    else:
        await message.answer(text=TEXTS['no_bookmarks'])


async def process_forward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_db[user_id]['page'] < len(book):
        user_db[user_id]['page'] += 1
        await callback.message.edit_text(
            **_get_page_content(user_id))
    await callback.answer()


async def process_backward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_db[user_id]['page'] > 1:
        user_db[user_id]['page'] -= 1
        await callback.message.edit_text(
            **_get_page_content(user_id)
        )
    await callback.answer()


async def process_page_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_db[user_id]['bookmarks'].add(user_db[user_id]['page'])
    await callback.answer(TEXTS['bookmark_added'])


async def process_bookmark_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_db[user_id]['page'] = int(callback.data)
    await callback.message.edit_text(
        **_get_page_content(user_id))
    await callback.answer()


async def process_edit_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        text=TEXTS[callback.data],
        reply_markup=create_edit_keyboard(
            *user_db[user_id]['bookmarks']))
    await callback.answer()


async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=TEXTS['cancel_text'])
    # await process_continue_command(callback)
    await callback.answer()


async def process_del_bookmark_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_db[user_id]['bookmarks'].remove(int(callback.data[:-3]))
    if user_db[user_id]['bookmarks']:
        await callback.message.edit_text(
            text=TEXTS['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *user_db[user_id]['bookmarks']))
    else:
        await callback.message.edit_text(text=TEXTS['no_bookmarks'])
    await callback.answer()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(
        process_beginning_command, commands=['beginning'])
    dp.register_message_handler(
        process_continue_command, commands=['continue'])
    dp.register_message_handler(
        process_bookmarks_command, commands=['bookmarks'])

    dp.register_callback_query_handler(process_forward_press, text='forward')
    dp.register_callback_query_handler(process_backward_press, text='backward')
    dp.register_callback_query_handler(
        process_page_press,
        lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    dp.register_callback_query_handler(
        process_bookmark_press,
        lambda x: x.data.isdigit())
    dp.register_callback_query_handler(
        process_edit_press,
        text='edit_bookmarks')
    dp.register_callback_query_handler(process_cancel_press, text='cancel')
    dp.register_callback_query_handler(
        process_del_bookmark_press,
        lambda x: 'del' in x.data and x.data[:-3].isdigit())
