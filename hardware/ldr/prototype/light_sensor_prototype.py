import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_ldr = 4


def main():

    while True:
        cup_detected = detect_light(pin_ldr)
        print(cup_detected)


def detect_light(pin):
    ldr_count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pin, GPIO.IN)

    # While the input pin reads 'off' or 'low' count is increased
    # If the pin reads 'off' or 'low' light source has decreased, a coffee cup is placed on the ldr
    while GPIO.input(pin) == GPIO.LOW:
        ldr_count += 1

    if ldr_count > 1500:
        return (True, ldr_count)  # cup detected (low light)
    else:
        return (False, ldr_count)  # no cup detected (bright light)


if __name__ == "__main__":
    main()