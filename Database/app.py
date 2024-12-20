from flask import Flask, render_template, redirect, request
from flask_mongoengine import MongoEngine
import mongoDB
from dotenv import load_dotenv
import os
from events import socketio

load_dotenv()

app = Flask(__name__)

database_URI = os.getenv("DATABASE_URI")
app.config["MONGODB_SETTINGS"] = {"host": database_URI}

db = MongoEngine()
db.init_app(app)
socketio.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


# show list of drinks, allow user to select a drink and click the next button to continue
@app.route("/drinks_selection")
def show_drinks_selection():
    all_drinks = mongoDB.view_all_drinks()
    print(all_drinks)
    return render_template("drinks_selection.html", all_drinks=all_drinks)


# show list of drinks , and temperature range for each drink (min and max temperatures)
@app.route("/temperatures")
def show_temperatures():
    all_temperatures = mongoDB.view_all_drinks()
    all_drinks = mongoDB.view_all_drinks()
    return render_template(
        "temperatures.html", all_temperatures=all_temperatures, all_drinks=all_drinks
    )


# show current drink name, temp and notification
@app.route("/barista_mode")
def barista_mode():
    current_drink_status = mongoDB.get_current_drink_status()
    print("current status", current_drink_status)
    return render_template(
        "barista_mode.html",
        current_drink_status=current_drink_status,
    )


@app.route("/get_drink_and_temperature", methods=["POST"])
def get_selected_drink():
    selected_drink = request.form.get("selected")
    current_temperature = request.form.get("pubnub_temperature")
    print("TEMPERATURE: ", current_temperature)
    current_temperature = int(current_temperature) * 2

    if selected_drink and current_temperature:
        mongoDB.add_drink_status(selected_drink, current_temperature)
        return redirect("/barista_mode")
    else:
        return "Please input the temperature and select a drink!"


@app.route("/barista_controls")
def barista_controls():
    return render_template("barista_controls.html")


@app.route("/add_drink")
def add_drink():
    return render_template("add_drink.html")


@app.route("/edit_drink")
def edit_drink():
    return render_template("edit_drink.html")


@app.route("/history")
def drink_history():
    all_drink_status = mongoDB.get_drink_status()
    return render_template(
        "history.html",
        all_drink_status=all_drink_status,
    )


# using the form action in the barista mode screen to get the show_coffee_data or no_coffee_data message
@app.route("/get_cup_detection", methods=["POST"])
def get_cup_detection():
    cup_detection_message = request.form.get("cup_detection")
    print(cup_detection_message)
    if cup_detection_message == "show_coffee_data":
        mongoDB.add_cup_detection("Cup detected")
        print("Message: cup detected")
        return redirect("/barista_mode")
    elif cup_detection_message == "no_coffee_data":
        mongoDB.add_cup_detection("No Cup detected")
        print("Message: no cup detected ")
        return redirect("/barista_mode")
    else:
        print("No message has been received")


if __name__ == "__main__":
    socketio.run(app, debug=True)
