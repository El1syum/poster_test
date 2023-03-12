import logging

from aiogram import types, Dispatcher
from bot.formater.formater import TextFormater


async def get_message(message: types.Message):
    from main import bot, POSTER_CHANNEL

    formater = TextFormater()

    logging.info(message)

    file_name = f"{message.photo[-1].file_unique_id}.jpg"
    file_path = f"media/{file_name}"
    if message.content_type == "photo":
        await message.photo[-1].download(file_path)

    caption = formater.channel_post(message.caption)

    photo = open(file_path, 'rb')

    await bot.send_photo(chat_id=POSTER_CHANNEL, photo=photo, caption=caption)


def register_get_message(dp: Dispatcher):
    dp.register_message_handler(get_message, content_types=["photo"])
