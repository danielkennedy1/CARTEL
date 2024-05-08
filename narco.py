from flask import Flask, request, Response
from schema import Schema, And, Use, Optional

from cartel.db import create_db
from cartel.users import register_user, list_users, get_user_by_name, get_user_by_id
from cartel.messages import list_messages, get_message, new_message

app = Flask(__name__)

# Validate request payload
schema_name_and_public_key = Schema(
    {"name": And(str, len), "public_key": And(str, len)})
schema_name = Schema({"name": And(str, len)})
schema_id = Schema({"id": And(Use(int), lambda n:  0 <= n)})
schema_user_id = Schema({"user_id": And(Use(int), lambda n:  0 <= n)})
schema_new_message = Schema({"sender": And(Use(int), lambda n:  0 <= n), "recipient": And(
    Use(int), lambda n:  0 <= n), "message": And(str, len), "signature": And(str, len), })
schema_message_id = Schema({"message_id": And(Use(int), lambda n:  0 <= n)})


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
        schema_name_and_public_key.validate(data)
        response = register_user(data["name"], data["public_key"])
    elif request.method == "POST":
        if data.get("id") is None:
            schema_name.validate(data)
            response = get_user_by_name(data["name"])
        else:
            print(data)
            schema_id.validate(data)
            response = get_user_by_id(data["id"])
    return response


# Messages: PUT to send a message
@app.route("/messages", methods=["PUT"])
def send_message():
    data: dict = request.json or {}
    schema_new_message.validate(data)
    return new_message(data)


# Messages: POST to get a specific message or a user's messages
@app.route("/messages", methods=["POST"])
def messages():
    data: dict = request.json or {}

    if schema_user_id.is_valid(data) and not schema_message_id.is_valid(data):
        return list_messages(data["user_id"])

    if schema_message_id.is_valid(data) and not schema_user_id.is_valid(data):
        return get_message(data["message_id"])

    return Response("Invalid payload", status=405)


if __name__ == '__main__':
    create_db(reset=True)
    app.run()
