import pytest
from light_sensor_prototype import detect_light

# ***  This tests is made with the intention of being ran in isolation ***


ldr_pin = 4 # adjust for your setup
# Before running this test ensure an object is placed over the Light Dependant Resistor
def test_cup_detected():
    detect_light(ldr_pin) = cup_result, pin_result
    print(f"cup_result: {cup_result}")
