import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import os, time
from dotenv import load_dotenv
from buzzer import Buzzer
import threading



load_dotenv()
pin_r = 16
pin_g = 20
pin_b = 21
leds = [pin_r, pin_g, pin_b]  # list of pins
keep_beeping = False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin_r, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_g, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_b, GPIO.OUT, initial=GPIO.LOW)


app_channel2 = "Get-notification"
class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f"Status: \n{status.category.name}")


config = PNConfiguration()
config.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
config.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
config.user_id = "Sipify"
pubnub = PubNub(config)
pubnub.add_listener(Listener())
subscription2 = pubnub.channel(app_channel2).subscription()



# The main function simulates data retrieval of temperature inputs and reacts accordingly
def handle_message(message):
    print("LED MESSAGE:" + message.message)
    coffee_notification = str(message.message)

    if coffee_notification == '"Drink while it\'s hot "':
        turn_on(pin_r)  # turn on red LED        - coffee is too hot
        pubnub.publish().channel(app_channel2).message("Red LED Activated").sync()
        keep_beeping = False

    elif coffee_notification == '"Reheat drink "':
        turn_on(pin_b)  # turn on blue LED       - coffee is too cold
        pubnub.publish().channel(app_channel2).message("Blue LED Activated").sync()
        keep_beeping = False

    elif coffee_notification == '"Ready to go! "':
        turn_on(pin_g)  # turn on green LED      - coffee is at optimal temperature
        pubnub.publish().channel(app_channel2).message("Green LED Activated").sync()

        keep_beeping = True # enable continuous beeping
        threading.Thread(target=beep_forever, daemon=True).start() # start buzzer beep on a thread

def main():
    try:
        subscription2.on_message = lambda message: handle_message(message)
        subscription2.subscribe()

        time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()


def turn_on(pin):
    global leds
    for led in leds:
        if led == pin:
            GPIO.output(pin, GPIO.HIGH)  # find the led that must be turned on
        else:
            turn_off(led)  # turn off other led that was previously on

def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)


buzzer = Buzzer(14)
# When keep_beeping becomes true, this function will continue to run inside a thread until it is set to false
def beep_forever():
    while keep_beeping:
        buzzer.beep(3)
        time.sleep(5)
