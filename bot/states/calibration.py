from aiogram.dispatcher.filters.state import StatesGroup, State


class CameraCalibration(StatesGroup):
    calibration_empty_bowl = State()
    calibration_full_bowl = State()


class Servo_calibration(StatesGroup):
    waiting_for_start = State()
    filling = State()
