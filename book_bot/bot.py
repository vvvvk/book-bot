import logging

from aiogram import Bot, Dispatcher

from book_bot.config import Config, load_config
from book_bot.handlers.other_handlers import register_echo_handlers
from book_bot.handlers.user_handlers import register_user_handlers
from book_bot.keyboards.main_menu_kb import set_main_menu


def register_all_handlers(dp: Dispatcher):
    register_user_handlers(dp)
    register_echo_handlers(dp)


async def main():
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s - %(name)s - %(message)s'
    )

    logger.info('Starting bot')
    cfg: Config = load_config()

    bot: Bot = Bot(cfg.bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot)

    await set_main_menu(dp)

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.close()
        logger.error('Bot stopped!')
