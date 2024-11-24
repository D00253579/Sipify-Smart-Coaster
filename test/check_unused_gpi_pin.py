import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# List of all available GPIO pins 
gpio_pins = [i for i in range(2, 28)]  

# List of used pins 
used_pins = [4, 17, 27, 22, 21]  

# Function to disable unused GPIO pins
def disable_unused_pins():
    for pin in gpio_pins:
        if pin not in used_pins:
            # Set unused pin as input with a pull-down resistor to avoid floating
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            print(f"Pin {pin} is disabled (set as input with pull-down).")

# Run the function to disable unused pins
if __name__ == "__main__":
    disable_unused_pins()
    GPIO.cleanup()
