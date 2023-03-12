import logging

from aiogram import types, Dispatcher


async def send_welcome(message: types.Message):
    logging.info(message)
    await message.reply(f'Hello, {message.from_user.full_name}!')


def register_welcome(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
