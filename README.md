# CARTEL

## User

### GET /user
returns all usernames

### PUT /user
Registers a new user
Accepts a JSON object with the following fields:
```
{
    "name": "username",
    "public_key": "pubkey"
    "password": "password"
}
```
Returns 
```
{
    "id": 1,
    "name": "username",
    "public_key": "pubkey"
}
```

### POST /user
Get user info from username

Accepts a JSON object with the following fields:
```
{
    "name": "username"
}
```
Returns 
```
{
    "id": 1,
    "name": "username",
    "public_key": "pubkey"
}
```

## Message

### PUT /message
Send a message
Accepts a JSON object with the following fields:
```
{
    "sender": 1,
    "recipient": 2,
    "password": "password",
    "message": "message1",
    "signature": "signature1",
    "nonce": 1,
    "passkey": "AAAAAA"

}
```
Returns 
```
{
    "id": 1,
    "sender": 1,
    "recipient": 2,
    "message": "message1",
    "signature": "signature1"
    "nonce": 1,
    "passkey": "AAAAAA"
}
```

### POST /message

Get messages for a given user id:
Accepts a JSON object with the following fields:
```
{
    "user_id": 1
}
```
Returns a list of message Ids
```
[ 2, 3, 4, 5]
```

### OR

Get a specific message:
```
{
    "message_id": 2
}
```

Returns the message: 
```
{
    "id": 2,
    "sender": 1,
    "recipient": 2,
    "message": "message1",
    "signature": "signature1"
    "passkey": "AAAAAA"
}
```
