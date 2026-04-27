import RPi.GPIO as GPIO

RED_PIN = 12
BLUE_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

pwm_red = GPIO.PWM(RED_PIN, 1000)
pwm_blue = GPIO.PWM(BLUE_PIN, 1000)

pwm_red.start(0)
pwm_blue.start(0)


def red(duty):
    pwm_red.ChangeDutyCycle(duty)
    pwm_blue.ChangeDutyCycle(0)


def blue(duty):
    pwm_red.ChangeDutyCycle(0)
    pwm_blue.ChangeDutyCycle(duty)


def both(red_duty, blue_duty):
    pwm_red.ChangeDutyCycle(red_duty)
    pwm_blue.ChangeDutyCycle(blue_duty)


def off():
    pwm_red.ChangeDutyCycle(0)
    pwm_blue.ChangeDutyCycle(0)

"""import lamper
import RPi.GPIO as GPIO
import time

lamper.red(30)
time.sleep(2)

lamper.blue(40)
time.sleep(2)

lamper.both(25, 25)
time.sleep(2)

lamper.off()

GPIO.cleanup()"""
