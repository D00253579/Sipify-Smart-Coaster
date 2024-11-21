from flask import Flask, render_template, redirect, request
import json

# import pymongo
import mongoDB
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# app.config["MONGODB_URI"] = (
# )

app.config["MONGODB_SETTINGS"] = {"db": "sipify", "host": "localhost", "port": 27017}

# mongoDB.db.init_app(app)

db = MongoEngine()
db.init_app(app)


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
    # drink_notification = mongoDB.get_notification()
    all_drink_status = mongoDB.get_drink_status()
    return render_template(
        "barista_mode.html",
        # drink_notification=drink_notification,
        all_drink_status=all_drink_status,
    )


@app.route("/get_drink_and_temperature", methods=["POST"])
def get_selected_drink():
    selected_drink = request.form.get("selected")
    current_temperature = request.form.get("input_temperature")

    current_temperature = int(current_temperature)

    if selected_drink and current_temperature:
        mongoDB.add_drink_status(selected_drink, current_temperature)
        return redirect("/barista_mode")
    else:
        return "Please input the temperature and select a drink!"


if __name__ == "__main__":
    app.run(debug=True)
