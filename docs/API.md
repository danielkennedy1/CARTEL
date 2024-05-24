# API Specification

## User

### GET `/user`

Returns all usernames as an array of strings

```python
["username1", "username2", "username3"]
```

### PUT `/user`

Registers a new user
Accepts a JSON object with the following fields:

```json
{
    "name": "username",
    "public_key": "pubkey"
    "password": "password"
}
```

**Returns**

```json
{
    "id": 1,
    "name": "username",
    "public_key": "pubkey"
}
```

### POST `/user`
Get user info from username

Accepts a JSON object with the following fields:

```json
{
    "name": "username"
}
```

**Returns**

```json
{
    "id": 1,
    "name": "username",
    "public_key": "pubkey"
}
```

## Message

### PUT `/message`

Send a message. Accepts a JSON object with the following fields:

```json
{
    "sender": 1,
    "recipient": 2,
    "password": "password",
    "message": "message1",
    "signature": "signature1",
    "nonce": "wuivcygawsui",
    "passkey": "AAAAAA",
    "tag": "tag1"

}
```

**Returns**

```json
{
    "id": 1,
    "sender": 1,
    "recipient": 2,
    "message": "message1",
    "signature": "signature1"
    "nonce": "wuivcygawsui",
    "passkey": "AAAAAA",
    "tag": "tag1"
}
```

### POST `/message`

Get messages for a given user id. Accepts a JSON object with the following fields:

```json
{
    "user_id": 1
}
```

**Returns a list of message IDs**

```json
[ 2, 3, 4, 5]
```

### OR

Get a specific message with a password. Accepts a JSON object with the following fields:

```json
{
    "message_id": 2,
    "password": "password"
}
```

**Returns the message:**

```json
{
    "id": 2,
    "sender": 1,
    "recipient": 2,
    "message": "message1",
    "signature": "signature1"
    "passkey": "AAAAAA",
    "tag": "tag1",
    "nonce": "wuivcygawsui"
}
```
