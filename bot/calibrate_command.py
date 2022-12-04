import asyncio
import json

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from datetime import datetime

from bot.keyboards.continue_kb import *
from bot.states.calibration import *
from rasp_devices.camera_features import save_picture
from rasp_devices.servo_features import set_servo_angle, servo_pin


async def calibrate_camera(message: Message):
    await message.answer(
        'Поставте порожню миску та закріпіть її, щоб вона не могла рухатись. Коли завершите приготування натисніть кнопку "продовжити"',
        reply_markup=continue_calibration_kb)
    print("here")
    await CameraCalibration.calibration_empty_bowl.set()


async def calibrate_empty(call: CallbackQuery, state: FSMContext):
    print("not here")
    await call.answer("Успішно відкалібрував пусту тарілку!")
    await asyncio.create_task(save_picture(image_path="images/empty_bowl.jpeg"))
    await call.message.answer(
        'Насипте мінімальну кількість корму, при якій бажаєте отримувати сповіщення про його закінчення, в миску та натисніть кнопку "продовжити"',
        reply_markup=continue_calibration_kb)
    await CameraCalibration.next()


async def calibrate_full(call: CallbackQuery, state: FSMContext):
    await call.answer("Успішно відкалібрував майже порожню тарілку!")
    await asyncio.create_task(save_picture(image_path="images/almost_empty_bowl.jpeg"))
    await state.finish()
    await call.message.answer("Калібрування завершено! Бажаєте переглянути зроблені фото?",
                              reply_markup=show_calibration_pics)


async def show_calibration(call: CallbackQuery):
    await call.answer()
    with open("images/empty_bowl.jpeg", "rb") as image:
        await call.message.answer_photo(image)
    with open("images/almost_empty_bowl.jpeg", "rb") as image:
        await call.message.answer_photo(image)
    await call.message.answer("Бажаєте провести калібрування знову?", reply_markup=redo_calibration)


async def calibrate_again(call: CallbackQuery):
    await calibrate_camera(call.message)


async def calibrate_servo(message: Message):
    await message.answer(
        'Поставте ємність з кормом над порожньою тарілкою. Після цього натисніть кнопку "Почати", розпочнеться наповнення тарілки, як тільки тарілка наповниться натисніть кнопку "Стоп".',
        reply_markup=start_calibration)
    await Servo_calibration.waiting_for_start.set()


async def servo_start(call: CallbackQuery, state: FSMContext):
    try:
        await set_servo_angle(servo_pin, 180)
    except RuntimeError:
        await state.finish()
        await call.answer("Здається хтось зараз калібрує наповнення або наповнює тарілку. Дочекайтесь поки інший завершить, якщо бажаєте встановити власне калібрування", show_alert=True)
        return
    await call.answer("Калібрування розпочато, натисніть кнопку 'Стоп', коли тарілка повністю напониться.")
    await state.update_data(start_time=datetime.now())
    await call.message.edit_reply_markup(reply_markup=stop_calibration)
    await Servo_calibration.next()


async def servo_stop(call: CallbackQuery, state: FSMContext):
    await call.answer("Успішно відкалібрував",show_alert=True)
    await set_servo_angle(servo_pin, 0)
    start_time = (await state.get_data())['start_time']
    duration = {"filling_duration": (datetime.now() - start_time).total_seconds()}
    with open("data/servo_dur.json", "w") as file:
        json.dump(duration, file)
    await call.message.delete()
    await state.finish()
