import time
import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from dotenv import load_dotenv
import os
import json

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
load_dotenv()
pin_ldr = 3
data = {}


class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f"Status: \n{status.category.name}")


config = PNConfiguration()
config.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
config.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
config.user_id = "Sipify"
pubnub = PubNub(config)
pubnub.add_listener(Listener())
app_channel = "Sipify-channel"
subscription = pubnub.channel(app_channel).subscription()
subscription.subscribe()
publish_result = (
    pubnub.publish().channel(app_channel).message("Hello from Sipify").sync()
)


def main():
    while True:
        time.sleep(3)
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
        pubnub.publish().channel(app_channel).message("Cup detected").sync()
        return (True, ldr_count)  # cup detected (low light)
    else:
        pubnub.publish().channel(app_channel).message("No cup detected").sync()
        return (False, ldr_count)  # no cup detected (bright light)


if __name__ == "__main__":
    main()
