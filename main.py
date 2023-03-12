import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from bot.handlers.start import register_welcome

if not os.path.exists('bot/logs/'):
    os.mkdir('bot/logs/')

logging.basicConfig(filename='bot/logs/bot.log', level=logging.INFO, encoding='utf-8')

TOKEN = dotenv_values('.env').get('TOKEN')


def register_all_handlers(dp):
    register_welcome(dp)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    register_all_handlers(dp)
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
