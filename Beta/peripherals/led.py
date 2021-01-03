# Libraries for all peripherals
import RPi.GPIO as GPIO

# Set up the LED with GPIO designators
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def led_on(pin, signal):

    if signal == 1:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
