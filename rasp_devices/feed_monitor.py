import asyncio
import aioschedule
from PIL import Image
from PIL import ImageChops
from PIL import ImageStat

from rasp_devices.camera_features import save_picture
notified = False
notified_about_empty = False


async def reset_notifications():
    global notified
    global notified_about_empty
    notified = False
    notified_about_empty = False


async def bowl_check(bot):
    global notified
    global notified_about_empty
    image_path = await asyncio.create_task(save_picture(image_path="images/current_bowl.jpeg"))
    im1 = Image.open("images/empty_bowl.jpeg")
    im2 = Image.open(image_path)
    im3 = Image.open("images/almost_empty_bowl.jpeg")

    diff = ImageChops.difference(im2, im1)
    diff2 = ImageChops.difference(im1, im3)
    stat = ImageStat.Stat(diff)
    stat2 = ImageStat.Stat(diff2)

    diff_ratio = sum(stat.mean) / (len(stat.mean) * 255) * 100
    diff2_ratio = sum(stat2.mean) / (len(stat2.mean) * 255) * 100
    print(diff_ratio, diff2_ratio)
    if diff_ratio <= diff2_ratio and not notified:
        await bot.send_message(chat_id=559346363, text=f"Миска майже порожня! Насипте корм!")
        notified = True
    if diff_ratio <= 1 and not notified_about_empty:
        await bot.send_message(chat_id=559346363, text=f"Миска порожня!")
        notified_about_empty = True
    await bot.send_message(chat_id=559346363,
                           text=f"Current difference is {diff_ratio}%, difference between calibrated bowls is {diff2_ratio}")


async def schedule_feed_check(bot):
    aioschedule.every().minute.do(bowl_check, bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
