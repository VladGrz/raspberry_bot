from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


continue_calibration_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продовжити", callback_data='continue'),
        ]
    ]
)

show_calibration_pics = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Показати фото", callback_data='show_pics'),
        ]
    ]
)

redo_calibration = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Відкалібрувати знову", callback_data='redo_calibration'),
        ]
    ]
)

start_calibration = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Почати", callback_data='start_calibration'),
        ]
    ]
)

stop_calibration = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Стоп", callback_data='stop_calibration'),
        ]
    ]
)