from cartel.db import User, session 
from flask import jsonify 
from sqlalchemy import select

# Register: create user, return created user data
# TODO: unique constraint on name, public_key
def register_user(name: str, public_key: str):
    user = User(name=name, public_key=public_key)
    session.add(user)
    session.commit()
    created_id = session.execute(select(User.id).where(User.name == name)).scalar() # type: ignore
    response = {"name": name, "public_key": public_key, "id": created_id}
    return jsonify(response)

# List users: return all user names
def list_users():
    usernames = session.execute(select(User.name)).scalars().all() # type: ignore
    return jsonify(usernames)

# Check public key: return user data
def get_user(name: str):
    # TODO: remove first when validation is added
    result = session.execute(select(User.id, User.public_key, User.name).where(User.name == name)).first() # type: ignore
    if not result:
        return jsonify({"error": "User not found"}), 404
    user = {
        "name": result.name,
        "public_key": result.public_key,
        "id": result.id
    }
    return jsonify(user)
