import bcrypt
from flask import jsonify 
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from cartel.db import User, session 

# Register: create user, return created user data
def register_user(name: str, public_key: str, password: str):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(name=name, public_key=public_key, password_hash=password_hash)
    try:
        session.add(user)
        session.commit()
    except IntegrityError: # Sqlalchemy error wrapper for unique constraint violation from DB
        return jsonify({"error": "User already exists"}), 400
    created_id = session.execute(select(User.id).where(User.name == name)).scalar() # type: ignore
    response = {"name": name, "public_key": public_key, "id": created_id}
    return jsonify(response)

# List users: return all user names
def list_users():
    usernames = session.execute(select(User.name)).scalars().all() # type: ignore
    return jsonify(usernames)

# Check public key: return user data
def get_user_by_name(name: str):
    #NOTE: the execute will only ever return one result, so we can use .first() instead of .all()
    result = session.execute(select(User.id, User.public_key, User.name).where(User.name == name)).first() # type: ignore
    if not result:
        return jsonify({"error": "User not found"}), 404
    user = {
        "name": result.name,
        "public_key": result.public_key,
        "id": result.id
    }
    return jsonify(user)

def get_user_by_id(id: int):
    result = session.execute(select(User.id, User.public_key, User.name).where(User.id == id)).first() # type: ignore
    if not result:
        return jsonify({"error": "User not found"}), 404
    user = {
        "name": result.name,
        "public_key": result.public_key,
        "id": result.id
    }
    return jsonify(user)

# Verify password
def verify_password(user_id: int, password: str) -> bool:
    result = session.execute(select(User.password_hash).where(User.id == user_id)).first() # type: ignore
    if not result:
        return False
    return bcrypt.checkpw(password.encode(), result.password_hash.encode())
