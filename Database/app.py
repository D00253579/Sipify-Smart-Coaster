from flask import Flask, render_template
import json

from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {"db": "sipify", "host": "localhost", "port": 27017}

db = MongoEngine()
db.init_app(app)

import mongoDB


@app.route("/")
def index():
    return render_template("index.html")


# show list of drinks, allow user to select a drink and click the next button to continue
@app.route("/drinks_selection")
def show_drinks_selection():
    all_drinks = mongoDB.view_all_drinks()
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
    all_drinks = mongoDB.view_all_drinks()
    all_notifications = mongoDB.view_all_notifications()
    print(all_notifications)
    return render_template(
        "barista_mode.html", all_drinks=all_drinks, all_notifications=all_notifications
    )


if __name__ == "__main__":
    app.run(debug=True)
