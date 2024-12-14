import RPi.GPIO
import time

class Buzzer:
    
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setmode(self.pin, GPIO.OUTPUT)

    def beep(self, duration=0.5):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup(self.pin)