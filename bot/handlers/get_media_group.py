import logging
from typing import List

from aiogram import Dispatcher, types
from aiogram.types import InputMediaPhoto

from bot.formater.formater import TextFormater


async def get_media_group(message: types.Message, album: List[types.Message]):
    from main import bot, CHANNELS

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

    for poster_channel in CHANNELS:
        await bot.send_media_group(chat_id=poster_channel, media=media_group)


def register_get_media_group(dp: Dispatcher):
    dp.register_message_handler(get_media_group, content_types=["photo"], is_media_group=True)
