from cartel.db import Message, session
from flask import Response, jsonify
from sqlalchemy import select


# List messages: return all messages
def list_messages(user_id: int):
    result = session.execute(select(Message.id, Message.sender).where(Message.recipient == user_id)).scalars().all() 
    if not result:
        return Response("No messages found", status=404)
    return jsonify(result) 

# Get message: return message data
def get_message(id: int):
    message = session.query(Message).get(id)
    if not message:
        return Response("Message not found", status=404)
    return jsonify({"id": message.id,
                    "sender": message.sender,
                    "recipient": message.recipient,
                    "message": message.message,
                    "signature": message.signature
                    })

# Send message: create message, return created message data
# TODO: Validate signature
def new_message(data: dict):
    message = Message(
            sender=data["sender"],
            recipient=data["recipient"],
            message=data["message"],
            signature=data["signature"])
    session.add(message)
    session.commit()
    return jsonify({"id": message.id,
                    "sender": message.sender,
                    "recipient": message.recipient,
                    "message": message.message,
                    "signature": message.signature
                    })
