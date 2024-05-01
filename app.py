from flask import Flask, request, Response
from cartel.db import create_db
from cartel.users import register_user, list_users, get_user
from cartel.messages import list_messages, get_message, new_message

app = Flask(__name__)

# TODO: Validation: https://flask-validates.readthedocs.io/en/latest/

# Users: GET to list all users
@app.route("/users", methods=["GET"])
def users():
    return list_users()

@app.route("/users", methods=["PUT", "POST"])
# Users: PUT to register, POST to get user
def register():
    data: dict = request.json or {}
    response = Response("Invalid method", status=405)
    if request.method == "PUT":
        response = register_user(data["name"], data["public_key"])
    elif request.method == "POST":
        response = get_user(data["name"])
    return response


# Messages: PUT to send a message
@app.route("/messages", methods=["PUT"])
def send_message():
    data: dict = request.json or {}
    return new_message(data)

@app.route("/messages", methods=["POST"])
def messages():
    data: dict = request.json or {}
    if data.get("message_id") is None:
        return list_messages(data["user_id"])
    return get_message(data["message_id"])

if __name__ == '__main__':
    create_db(reset=True)
    app.run()

