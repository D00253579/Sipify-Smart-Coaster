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
    mongoDB.getAllDrinks()
    print("1", mongoDB.viewAllDrinks())
    return render_template("index.html", all_drinks=mongoDB.getAllDrinks())


if __name__ == "__main__":
    # latte = Drink(name="Latte")
    # latte.save()
    # print("Document created successfully")
    # app.run(debug=True, host="0.0.0")
    app.run(debug=True)
