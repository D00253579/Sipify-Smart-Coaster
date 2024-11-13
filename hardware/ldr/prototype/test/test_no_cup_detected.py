import pytest
from light_sensor_prototype import detect_light

# ***  This tests is made with the intention of being ran in isolation ***


ldr_pin = 4  # adjust for your setup


# Before running this test ensure no object is placed over the Light Dependant Resistor
def test_no_cup_detected():
    assert detect_light(ldr_pin) == False
