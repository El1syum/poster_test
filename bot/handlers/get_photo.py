import logging

from aiogram import types, Dispatcher

from bot.formater.formater import TextFormater


async def get_photo(message: types.Message):
    from main import bot, CHANNELS

    formater = TextFormater()

    logging.info(message)

    file_name = f"{message.photo[-1].file_unique_id}.jpg"
    file_path = f"media/{file_name}"
    if message.content_type == "photo":
        await message.photo[-1].download(file_path)

    try:
        caption = formater.channel_post(message.caption)
    except AttributeError:
        caption = ''

    photo = open(file_path, 'rb')

    for poster_channel in CHANNELS:
        await bot.send_photo(chat_id=poster_channel, photo=photo, caption=caption)


def register_get_photo(dp: Dispatcher):
    dp.register_message_handler(get_photo, content_types=["photo"])
