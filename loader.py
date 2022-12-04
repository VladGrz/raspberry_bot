from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from bot.basic_commands import start_command, take_picture, help_command
from bot.fill_bowl_command import fill_bowl
from bot.calibrate_command import *
from bot.states.calibration import *
from rasp_devices.feed_monitor import schedule_feed_check

# Defining storage to store info about citation in states
storage = MemoryStorage()

# Creating basic object of the Bot
# using which we will connect to the Telegram Bot API
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)  # Creating object which will process incoming updates


async def on_start(x):
    asyncio.create_task(schedule_feed_check(bot))


# Registering handlers for different types of updates
dp.register_message_handler(start_command, commands=["start"])
dp.register_message_handler(help_command, commands=["help"])
dp.register_message_handler(take_picture, commands=["take_picture"])
dp.register_message_handler(calibrate_camera, commands=["calibrate"], state='*')
dp.register_message_handler(calibrate_servo, commands=["calibrate_filling"])
dp.register_message_handler(fill_bowl, commands=["fill_bowl"])
dp.register_callback_query_handler(calibrate_empty,
                                   lambda c: c.data == "continue",
                                   state=CameraCalibration.calibration_empty_bowl)
dp.register_callback_query_handler(calibrate_full,
                                   lambda c: c.data == "continue",
                                   state=CameraCalibration.calibration_full_bowl)
dp.register_callback_query_handler(show_calibration,
                                   lambda c: c.data == "show_pics")
dp.register_callback_query_handler(calibrate_again,
                                   lambda c: c.data == "redo_calibration")
dp.register_callback_query_handler(servo_start,
                                   lambda c: c.data == "start_calibration",
                                   state=Servo_calibration.waiting_for_start)
dp.register_callback_query_handler(servo_stop,
                                   lambda c: c.data == "stop_calibration",
                                   state=Servo_calibration.filling)
