import RPi.GPIO as GPIO
import time

class Buzzer:
    
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def beep(self, repeat):
        for i in range(0, repeat):
            for pulse in range(60):
                GPIO.output(self.pin, True)
                time.sleep(0.001)
                GPIO.output(self.pin, False)
                time.sleep(0.001)
            time.sleep(0.02)

    def cleanup(self):
        GPIO.cleanup(self.pin)
