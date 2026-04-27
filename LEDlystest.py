import RPi.GPIO as GPIO
import time

RED_PIN = 12
BLUE_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

pwm_red = GPIO.PWM(RED_PIN, 1000)
pwm_blue = GPIO.PWM(BLUE_PIN, 1000)

pwm_red.start(0)
pwm_blue.start(0)

try:
    # Test rød alene
    print("Rød test")
    for duty in [10, 20, 30, 40]:
        print(f"Rød {duty}%")
        pwm_red.ChangeDutyCycle(duty)
        pwm_blue.ChangeDutyCycle(0)
        time.sleep(3)

    pwm_red.ChangeDutyCycle(0)
    time.sleep(2)

    # Test blå alene
    print("Blå test")
    for duty in [10, 20, 30, 40]:
        print(f"Blå {duty}%")
        pwm_red.ChangeDutyCycle(0)
        pwm_blue.ChangeDutyCycle(duty)
        time.sleep(3)

    pwm_blue.ChangeDutyCycle(0)
    time.sleep(2)

    # Test begge sammen (forsigtigt)
    print("Begge test (lav belastning)")
    pwm_red.ChangeDutyCycle(30)
    pwm_blue.ChangeDutyCycle(30)
    time.sleep(5)

    print("Slukker")
    pwm_red.ChangeDutyCycle(0)
    pwm_blue.ChangeDutyCycle(0)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    pwm_red.ChangeDutyCycle(0)
    pwm_blue.ChangeDutyCycle(0)
    pwm_red.stop()
    pwm_blue.stop()
    GPIO.cleanup()