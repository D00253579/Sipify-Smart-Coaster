import os
import glob
import time

import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from dotenv import load_dotenv


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
load_dotenv()
pin_ldr = 4
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
os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

# Locate sensor output file
base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"


# Opens the sensors output file and reads in the line for parsing, is stored as a list where the
# the second index contains the temperature data
def read_temp_raw():
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    temp_data = lines[1]
    # lines[1] contains a string with a unique identifier for the sensor, followed by t=xxxx, where xxxx = some temperature
    # I split this string at the = and the second element is the temperature with no decimal place. By taking the first 2 digits I get
    # the celsius value as a whole number.

    # **** This approach limits the sensor to only read valid values up to 99 ****
    temperature = temp_data.split("=")[1][:2]
    return temperature


while True:
    if read_temp() != "":
        pubnub.publish().channel(app_channel).message(read_temp()).sync()

    print(read_temp())
    time.sleep(1)
