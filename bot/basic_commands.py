import asyncio

from aiogram.types import Message

from rasp_devices.camera_features import save_picture
from bot.extract_info_from_command import extract_params


async def start_command(message: Message):
    await message.answer("hello")


async def take_picture(message: Message):
    options = await asyncio.create_task(extract_params(message.text))

    rotate = options.get("-rotate")
    rotate = int(rotate) if rotate else None
    text = options.get("-text")
    brightness = options.get("-brightness")
    brightness = int(brightness) if brightness else None
    res_x = options.get("-res_x")
    res_y = options.get("-res_y")
    res_x = int(res_x) if res_x else None
    res_y = int(res_y) if res_y else None

    text_size = options.get("-text_size")
    text_size = int(text_size) if text_size else None
    text_color = options.get("-text_color")
    text_background = options.get("-text_background")
    effect = options.get("-effect")
    exposure_mode = options.get("-exposure_mode")
    awb_mode = options.get("-awb_mode")

    image_path = await asyncio.create_task(
        save_picture(rotate=rotate, text=text, text_size=text_size, text_color=text_color,
                     text_background=text_background, effect=effect, exposure_mode=exposure_mode, awb_mode=awb_mode,
                     brightness=brightness, res_x=res_x, res_y=res_y))

    with open(image_path, "rb") as image:
        await message.answer_photo(image)
