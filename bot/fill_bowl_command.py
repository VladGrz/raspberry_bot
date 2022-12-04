import asyncio
import json

from aiogram.types import Message

from bot.extract_info_from_command import extract_params
from rasp_devices.feed_monitor import reset_notifications
from rasp_devices.servo_features import set_servo_angle, servo_pin


async def fill_bowl(message: Message):
    options = await asyncio.create_task(extract_params(message.text))
    amount = options.get("-amount")
    with open("data/servo_dur.json", "r") as file:
        duration = json.load(file)["filling_duration"] - 0.6
    if amount is not None:
        duration = duration * (float(amount) / 100)
    message_to_user = await message.answer("Наповнюю тарілку...")
    filled = 0
    try:
        await asyncio.create_task(set_servo_angle(servo_pin, 180))
    except RuntimeError:
        await message.answer("Хтось вже наповнює тарілку. Перевірте за допомогою /take_picture.")
        await message_to_user.delete()
    else:
        for i in range(4):
            await message_to_user.edit_text(f"Йде процес наповнення: {filled}%")
            filled += 25
            await asyncio.sleep(duration / 4)
        await asyncio.create_task(set_servo_angle(servo_pin, 0))
        await message_to_user.edit_text(f"Завершив наповнення тарілки!")
        await reset_notifications()
