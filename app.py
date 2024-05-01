from flask import Flask, request, Response
from cartel.db import create_db
from cartel.users import register_user, list_users, get_user
from cartel.messages import list_messages, get_message, send_message

app = Flask(__name__)

# TODO: Validation: https://flask-validates.readthedocs.io/en/latest/

# Users: GET to list all users
@app.route("/users", methods=["GET"])
def users():
    return list_users()

@app.route("/users", methods=["PUT", "POST"])
# Users: PUT to register, POST to check public key of a user
def register():
    data: dict = request.json or {}
    response = Response("Invalid method", status=405)
    if request.method == "PUT":
        response = register_user(data["name"], data["public_key"])
    elif request.method == "POST":
        response = get_user(data["name"])
    return response


# Messages: GET to list all messages, POST to check a message, PUT to send a message
@app.route("/messages", methods=["GET", "POST", "PUT"])
def messages():
    data: dict = request.json or {}
    response = Response("Invalid method", status=405)
    if request.method == "GET":
        response = list_messages(data["public_key"])
    elif request.method == "POST":
        response = get_message(data["id"])
    elif request.method == "PUT":
        response = send_message(data)
    return response

if __name__ == '__main__':
    create_db(reset=True)
    app.run()

