import asyncio
from picamera import PiCamera, Color


async def save_picture(rotate=None, text=None, text_size=None, text_color=None,
                       text_background=None, effect=None, exposure_mode="auto", awb_mode="auto",
                       brightness=None, res_x=None, res_y=None, image_path="images/image.jpg"):
    with PiCamera() as camera:
        if res_x is None:
            res_x = 2592
        if res_y is None:
            res_y = 1944

        camera.resolution = (res_x, res_y)
        camera.image_effect = effect if effect is not None else "none"
        camera.exposure_mode = exposure_mode if exposure_mode is not None else "auto"
        camera.awb_mode = awb_mode if awb_mode is not None else "auto"
        if rotate:
            camera.rotation = rotate
        if brightness:
            camera.brightness = brightness
        if text:
            camera.annotate_text_size = text_size if text_size is not None else 60
            camera.annotate_foreground = Color(text_color) if text_color is not None else Color("white")
            if camera.annotate_background is not None:
                camera.annotate_background = Color(text_background)
            camera.annotate_text = text
        camera.capture(image_path)
    return image_path


async def save_video(rotate=None, text=None, brightness=None, res_x=None, res_y=None, video_path="videos/video"):
    pass
