import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, types

from bot.handlers.get_media_group import register_get_media_group
from bot.handlers.get_photo import register_get_photo
from bot.handlers.start import register_welcome
from bot.middleware.album import AlbumMiddleware

if not os.path.exists('bot/logs/'):
    os.mkdir('bot/logs/')

if not os.path.exists('media/'):
    os.mkdir('media/')

logging.basicConfig(filename='bot/logs/bot.log', level=logging.INFO, encoding='utf-8')

try:
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError('Create a config.json!')

TOKEN = config.get('TOKEN')
CHANNELS = config.get('CHANNEL_LOGIN')

bot = Bot(token=TOKEN)


def register_all_handlers(dp):
    register_welcome(dp)
    register_get_media_group(dp)
    register_get_photo(dp)


def register_all_middleware(dp):
    dp.middleware.setup(AlbumMiddleware())


async def setup_bot_commands(dp):
    bot_commands = [
        types.BotCommand(command="/start", description="Start polling"),
        types.BotCommand(command="/help", description="Get info about me"),
    ]
    await dp.bot.set_my_commands(bot_commands)


async def main():
    dp = Dispatcher(bot)
    register_all_handlers(dp)
    register_all_middleware(dp)
    await setup_bot_commands(dp)
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped!')
