from schema import Schema, And, Use

valid_name_and_public_key = Schema(
    {"name": And(str, len), "public_key": And(str, len), "password": And(str, len)}
)
valid_name = Schema({"name": And(str, len)})
valid_id = Schema({"id": And(Use(int), lambda n: 0 <= n)})
valid_user_id = Schema({"user_id": And(Use(int), lambda n: 0 <= n)})
valid_new_message = Schema(
    {
        "sender": And(Use(int), lambda n: 0 <= n),
        "recipient": And(Use(int), lambda n: 0 <= n),
        "message": And(str, len),
        "signature": And(str, len),
        "password": And(str, len),
        "iv": And(str, len),
        "secret": And(str, len),
    }
)
valid_message_id = Schema({"message_id": And(Use(int), lambda n: 0 <= n)})
