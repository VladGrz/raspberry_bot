import asyncio

from aiogram.types import Message

from rasp_devices.camera_features import save_picture
from bot.extract_info_from_command import extract_params


async def start_command(message: Message):
    await message.answer("Привіт! Я бот, який призначений для моніторингу тарілки твого домашнього улюбленця, а також спостереження за ним(тільки йому про це не кажи🤫). Для детальнішої інформації про мою роботу тицяй /help")


async def help_command(message: Message):
    await message.answer("Всього є 4 основних команди: /take_picture, /fill_bowl, /calibrate_bowl, /calibrate_filling."
                         "\nОстанні дві достатньо надіслати мені і далі слідувати інструкціям, "
                         "перші ж дві мають свої особливості. "
                         "\nДля початку /fill_bowl може бути використана без додаткових параметрів, в такому випадку "
                         "буде насипана максимальна відкалібрована кількість корму, або ж з параметром -amount. " 
                         "Якщо вказується параметр то через пробіл після нього вказується значення, "
                         "для даної команди доступні значення від 0 до 100(де 100 - повна тарілка, 50 - половина, і тд)"
                         "\nКоманда /take_picture схожа за синтаксисом до попередньої. Дотупні параметри: -rotate, "
                         "-text, -brightness, -text_size, -text_color, -text_background, -effect, -exposure_mode, "
                         "-awb_mode, -res_x, -res_y. Значення -text параметра може бути неперервана пробілами стрічка"
                         "(приклад_неперервної_стрічки), або, якщо в тексті є пробіли, його варто обгорнути в подвійні лапки. "
                         "Колір тексту та його фону має бути заданий словесно, наприклад red і тд. Стандартні -rotate "
                         "значення -rotate: 0, 90, 180, 270, 360; -brightness: 0-100(за замовчуванням 50); -text_size: "
                         "6-160. <a href='https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7'>Детальніше про значення інших параметрів.</a>",
                         parse_mode='html',
                         disable_web_page_preview=True
                         )

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
