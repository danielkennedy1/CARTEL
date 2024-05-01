from cartel.db import User, Message
from flask import Response

# List messages: return all messages
def list_messages(public_key: str):
    return Response("Success", status=200) 

# Check message: return message data
def get_message(id: int):
    return Response("Success", status=200) 

# Send message: create message, return created message data
def send_message(data: dict):
    return Response("Success", status=200) 
