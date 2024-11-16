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


class Notifications(db.Document):
    status = db.StringField()


# Create a drink history class from db
# Include the current temperature - to take this in
# The drink name that was selected from the drinks selection page
# The notification associated with it


# Use a dictionary to store the list of drinks
# access each variable using the name in quotation marks
def view_all_drinks():
    drink_records = {"drinks": []}
    for drink in Drinks.objects:
        drink_records["drinks"].append(
            {
                "drink_name": drink.drink_name,
                "temperature_type": drink.temperature_type,
                "minimum_temperature": drink.minimum_temperature,
                "maximum_temperature": drink.maximum_temperature,
            }
        )
        # print the drink values to view in terminal
        print(
            str(drink.drink_name)
            + " | "
            + str(drink.temperature_type)
            + " | "
            + str(drink.minimum_temperature)
            + " | "
            "" + str(drink.maximum_temperature)
        )
    return drink_records


def view_all_notifications():
    notification_records = {"notifications": []}
    for notification in Notifications.objects:
        notification_records["notifications"].append({"message": notification.message})
    return notification_records


# notifications based on temperature ranges
