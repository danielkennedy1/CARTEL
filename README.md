# CARTEL

## User

# GET /user
returns all usernames

# PUT /user
Registers a new user
Accepts a JSON object with the following fields:
```
{
    "name": "username",
    "public_key": "pubkey"
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

# POST /user
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
