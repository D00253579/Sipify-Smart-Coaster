import time
import RPi.GPIO as GPIO

pin_r = 21
pin_g = 20
pin_b = 16
leds = [pin_ddr, pin_g, pin_b]  # list of pins



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin_r, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_g, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_b, GPIO.OUT, initial=GPIO.LOW)

# These values would change depending on what coffee type is currently selected
min_temp = 0
max_temp = 0
# optimal_temp = (>= min_temp && <= max_temp)



# The main function simulates data retrival of temperature inputs and reacts accordingly
def main():
    try:
        while True:
   
            if coffee_temp > max_temp:
                turn_on(pin_r) # turn on red LED        - coffee is too hot
    
            elif coffee_temp < min_temp:
                turn_on(pin_b) # turn on blue LED       - coffee is too cold

            else:
                turn_on(pin_g) # turn on green LED      - coffee is at optimal temperature
    
    except KeyboardException:
        GPIO.cleanup()


def turn_on(pin):
    global leds
    for led in leds:
        if led == pin:
            GPIO.output(pin, GPIO.HIGH) # find the led that must be turned on
        else:
            turn_off(led) # turn off other led that was previously on


def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)


if __name__ == "__main__":
    main()
