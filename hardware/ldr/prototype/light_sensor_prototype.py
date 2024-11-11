import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinldr = 4


def detect_light():
    ldrcount = 0
    GPIO.setup(pinldr, GPIO.OUT)
    GPIO.output(pinldr, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pinldr, GPIO.IN)

    # While the input pin reads 'off' or 'low' count is increased
    # If the pin reads 'off' or 'low' light source has decreased, a coffee cup is placed on the ldr
    while(GPIO.input(pinldr) == GPIO.LOW):
        ldrcount += 1
    return ldrcount

while True:
    print(detect_light())
    time.sleep(1) # allow capacitor to decharge
