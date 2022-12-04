import asyncio

from aiogram import executor

from loader import dp, on_start

if __name__ == '__main__':
    # Starting bot in long-polling mode
    executor.start_polling(dp, on_startup=on_start, skip_updates=True)
