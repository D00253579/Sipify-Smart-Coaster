from flask_mongoengine import MongoEngine

from app import db


# client = pymongo.MongoClient(CONNECTION_STRING)


# db = client.get_database("Sipify")

# db = MongoEngine(app)


# drink class is for the drinks table
class Drinks(db.Document):
    drink_name = db.StringField()
    temperature_type = db.StringField()  # hot or cold drink
    minimum_temperature = db.IntField()
    maximum_temperature = db.IntField()


# new_drink = Drink(coffee_name="Latte")


def viewAllDrinks():
    print("view all drinks called")
    for drink in Drinks.objects:
        # print(
        #     f"{drink.drink_name} + {drink.temperature_type} + {drink.minimum_temperature} + {drink.maximum_temperature}"
        # )
        print(
            str(drink.drink_name)
            + " | "
            + str(drink.temperature_type)
            + " | "
            + str(drink.minimum_temperature)
            + " | "
            "" + str(drink.maximum_temperature)
        )


def getAllDrinks():
    drink_records = {"drinks": []}
    for drink in Drinks.objects:
        drink_records["drinks"].append(
            [
                drink.drink_name,
                drink.temperature_type,
                drink.minimum_temperature,
                drink.maximum_temperature,
            ]
        )
    return drink_records
