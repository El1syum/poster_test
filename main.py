import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher

from bot.handlers.get_message import register_get_message
from bot.handlers.start import register_welcome
from bot.middleware.album import AlbumMiddleware

if not os.path.exists('bot/logs/'):
    os.mkdir('bot/logs/')

if not os.path.exists('media/'):
    os.mkdir('media/')

logging.basicConfig(filename='bot/logs/bot.log', level=logging.INFO, encoding='utf-8')

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)


TOKEN = config.get('TOKEN')
CHANNELS = config.get('CHANNEL_LOGIN')
POSTER_CHANNEL = CHANNELS[0]

bot = Bot(token=TOKEN)


def register_all_handlers(dp):
    register_welcome(dp)
    register_get_message(dp)


def register_all_middleware(dp):
    dp.middleware.setup(AlbumMiddleware())


async def main():
    dp = Dispatcher(bot)
    register_all_handlers(dp)
    register_all_middleware(dp)
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
