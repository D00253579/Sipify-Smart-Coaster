from extensions import socketio
from flask import render_template
import mongoDB
import time


@socketio.on("connect")
def handle_connect():
    print("Socket connected!")


@socketio.on("updateTemp")
def update_temperature(selectedDrink, newTemp):
    print("USERS SELECTED DRINK: ", selectedDrink)
    print("NEW TEMPERATURE: ", newTemp)
    mongoDB.add_drink_status(selectedDrink, newTemp)
