from flask import Response, jsonify
from sqlalchemy import select
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from cartel.db import Message, User, session
from cartel.users import verify_password


# List messages: return all messages for user
def list_messages(user_id: int):
    result = session.execute(select(Message.id, Message.sender).where(Message.recipient == user_id)).scalars().all() 
    if not result:
        return Response("No messages found", status=404)
    return jsonify(result) 

# Get message: return message data by ID
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
def new_message(data: dict):

    if not verify_password(data["sender"], data["password"]):
        return Response("Access denied: password is incorrect", status=401)

    if not session.query(User).get(data["recipient"]):
        return Response("Recipient not found", status=404)
    
    # verify the signature
    sender_pubkey = session.execute(select(User.public_key).where(User.id == data["sender"])).scalar() # type: ignore

    if not sender_pubkey:
        return Response("Sender ID is not found", status=404)

    sender_pubkey = RSA.import_key(sender_pubkey)

    hash = SHA256.new(bytes.fromhex(data["message"]))

    try:
        pkcs1_15.new(sender_pubkey).verify(hash, bytes.fromhex(data["signature"]))
    except ValueError as e:
        return Response(f"Signature is invalid {e}", status=400)

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
