from schema import Schema, And

valid_name_and_public_key = Schema(
    {
        "name": And(str, len),
        "public_key": And(str, len),
        "password": And(str, len)
    }
)
valid_name = Schema(
        {
            "name": And(str, len)
        }
)
valid_id = Schema(
        {
            "id": And(int, lambda n:  0 <= n)
        }
)
valid_user_id = Schema(
        {
            "user_id": And(int, lambda n:  0 <= n)
        }
)
valid_new_message = Schema(
        {
            "sender": And(int, lambda n:  0 <= n),
            "recipient": And(int, lambda n:  0 <= n),
            "message": And(str, len),
            "signature": And(str, len),
            "password": And(str, len),
            "nonce": And(int, lambda n:  0 <= n),
            "passkey": And(str, len),
        }
)
valid_read_message = Schema(
    {
        "message_id": And(int, lambda n:  0 <= n),
        "password": And(str, len)
    }
)
