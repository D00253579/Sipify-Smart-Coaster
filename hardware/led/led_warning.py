import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
import os, time
from dotenv import load_dotenv

load_dotenv()
pin_r = 21
pin_g = 20
pin_b = 16
leds = [pin_r, pin_g, pin_b]  # list of pins


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin_r, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_g, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_b, GPIO.OUT, initial=GPIO.LOW)


class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f"Status: \n{status.category.name}")


config = PNConfiguration()
config.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
config.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
config.user_id = "Sipify"
pubnub = PubNub(config)
pubnub.add_listener(Listener())
app_channel1 = "Sipify-channel"
app_channel2 = "Get-notification"
subscription1 = pubnub.channel(app_channel1).subscription()
subscription1.on_message = lambda message: handle_message(message)
subscription1.subscribe()
subscription2 = pubnub.channel(app_channel2).subscription()
subscription2.on_message = lambda message: handle_message(message)
subscription2.subscribe()

publish_result = (
    pubnub.publish().channel(app_channel1).message("Hello from Sipify").sync(),
    pubnub.publish().channel(app_channel2).message("Hello from Sipify").sync(),
)


# The main function simulates data retrieval of temperature inputs and reacts accordingly
def handle_message(message):
    print(message.message)
    coffee_notification = message.message

    while True:
        if coffee_notification == "Drink while it's hot":
            turn_on(pin_r)  # turn on red LED        - coffee is too hot
            # pubnub.publish().channel(app_channel2).message("Red LED Activated").sync()
            break
        elif coffee_notification == "Reheat drink":
            turn_on(pin_b)  # turn on blue LED       - coffee is too cold
            # pubnub.publish().channel(app_channel2).message("Blue LED Activated").sync()
            break
        elif coffee_notification == "Ready to go!":
            turn_on(pin_g)  # turn on green LED      - coffee is at optimal temperature
            # pubnub.publish().channel(app_channel2).message("Green LED Activated").sync()
            break

        else:
            # pubnub.publish().channel(app_channel2).message("Incorrect Message").sync()
            break
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
    pubnub.publish().channel(app_channel2).message("LED deactivated").sync()
