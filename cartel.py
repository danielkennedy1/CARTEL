from flask import Flask, request, Response

from cartel.db import create_db
from cartel.users import register_user, list_users, get_user_by_name, get_user_by_id
from cartel.messages import list_messages, get_message, new_message
from cartel.schemas import valid_id, valid_user_id, valid_name, valid_name_and_public_key, valid_message_id, valid_new_message

app = Flask(__name__)

# Users: GET to list all users
@app.route("/users", methods=["GET"])
def users():
    return list_users()


# Users: PUT to register, POST to get user
@app.route("/users", methods=["PUT", "POST"])
def register():
    data: dict = request.json or {}
    response = Response("Invalid method", status=405)
    if request.method == "PUT":
        valid_name_and_public_key.validate(data)
        response = register_user(data["name"], data["public_key"], data["password"])
    elif request.method == "POST":
        if data.get("id") is None:
            valid_name.validate(data)
            response = get_user_by_name(data["name"])
        else:
            print(data)
            valid_id.validate(data)
            response = get_user_by_id(data["id"])
    return response


# Messages: PUT to send a message
@app.route("/messages", methods=["PUT"])
def send_message():
    data: dict = request.json or {}
    valid_new_message.validate(data)
    return new_message(data)


# Messages: POST to get a specific message or a user's messages
@app.route("/messages", methods=["POST"])
def messages():
    data: dict = request.json or {}

    if valid_user_id.is_valid(data) and not valid_message_id.is_valid(data):
        return list_messages(data["user_id"])

    if valid_message_id.is_valid(data) and not valid_user_id.is_valid(data):
        return get_message(data["message_id"])

    return Response("Invalid payload", status=405)


if __name__ == '__main__':
    create_db(reset=True)
    app.run()
