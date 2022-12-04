import asyncio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)  # white => TILT


async def set_servo_angle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    duty_cycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(duty_cycle)
    await asyncio.sleep(0.3)
    pwm.stop()
