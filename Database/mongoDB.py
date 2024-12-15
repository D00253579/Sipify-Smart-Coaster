from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField
import base64
import datetime

from app import db


# drink class is for the drinks table
class Drinks(db.Document):
    meta = {"collection": "drinks"}
    drink_name = db.StringField()
    temperature_type = db.StringField()  # hot or cold drink
    minimum_temperature = db.IntField()
    maximum_temperature = db.IntField()


class Notifications(db.Document):
    meta = {"collection": "notifications"}
    status = db.StringField()
    message = db.StringField()


# Create a drink history class from db
# Include the current temperature - to take this in
# The drink name that was selected from the drinks selection page
# The notification associated with it
class Drink_Status(db.Document):
    meta = {"collection": "drink_status"}
    selected_drink = db.StringField()
    current_temperature = db.IntField()
    current_notification = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now)


class Cup_Detection(db.Document):
    meta = {"collection": "cup_detection"}
    message = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now)


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
    print(drink_records)

    return drink_records


def view_all_notifications():
    notification_records = {"notifications": []}
    for notification in Notifications.objects:
        notification_records["notifications"].append(
            {"status": notification.status, "message": notification.message}
        )
    return notification_records


# notifications based on temperature ranges
def get_notification(selected_drink, current_temperature):
    for drink in Drinks.objects:
        if (
            drink.drink_name == selected_drink
        ):  # find the matching drink name from the table
            if int(current_temperature) < drink.minimum_temperature:  # drink is cold
                notification = Notifications.objects.get(status="cold")
            elif int(current_temperature) > drink.maximum_temperature:  # drink is hot
                notification = Notifications.objects.get(status="hot")
            else:
                notification = Notifications.objects.get(
                    status="ready"
                )  # drink is ready

            if notification:
                return (
                    notification.message
                )  # output the message associated with the status
            else:
                return "Notification not available"


# make sure to have the barista mode to display the most recent drink that has been added into the drink status table
# or use the sessions
def get_drink_status():
    drink_status_records = {"status": []}
    for status in Drink_Status.objects:
        drink_status_records["status"].append(
            {
                "selected_drink": status.selected_drink,
                "current_temperature": status.current_temperature,
                "current_notification": status.current_notification,
            }
        )
    return drink_status_records


# get the most recent drink status to display on the barista mode page
def get_current_drink_status():
    current_drink_status = Drink_Status.objects.order_by(
        "-created_at"
    ).first()  # descending order

    return {
        "current_status": [
            {
                "selected_drink": current_drink_status.selected_drink,
                "current_temperature": current_drink_status.current_temperature,
                "current_notification": current_drink_status.current_notification,
            }
        ]
    }


def add_drink_status(selected_drink, current_temperature):
    if selected_drink is not False:
        # take in the notification from the get notification method
        current_notification = get_notification(selected_drink, current_temperature)

        Drink_Status(
            selected_drink=selected_drink,
            current_temperature=int(current_temperature),
            current_notification=current_notification,
        ).save()

        print(
            str(selected_drink)
            + " | "
            + str(current_temperature)
            + " | "
            + str(current_notification)
        )
    else:
        print("No drink selected")


def add_cup_detection(cup_detection_message):
    if cup_detection_message is not False:
        Cup_Detection(
            message=cup_detection_message, created_at=datetime.datetime.now()
        ).save()
        print("Cup message received")
        print(str(cup_detection_message))
    else:
        print("No message for cup detection")
