import logging
from typing import List

from aiogram import types, Dispatcher
from aiogram.types import InputMediaPhoto

from bot.formater.formater import TextFormater


async def get_media_group(message: types.Message, album: List[types.Message]):
    from main import bot, POSTER_CHANNEL

    media_group = types.MediaGroup()

    formater = TextFormater()

    logging.info(message)

    for obj in album:
        file_name = f"{obj.photo[-1].file_unique_id}.jpg"
        file_path = f"media/{file_name}"
        await obj.photo[-1].download(file_path)

        try:
            caption = formater.channel_post(obj.caption)
        except AttributeError:
            caption = ''

        media_group.attach(InputMediaPhoto(open(file_path, 'rb'), caption=caption))

    await bot.send_media_group(chat_id=POSTER_CHANNEL, media=media_group)


async def get_photo(message: types.Message):
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
    dp.register_message_handler(get_media_group, content_types=["photo"], is_media_group=True)
    dp.register_message_handler(get_photo, content_types=["photo"])
