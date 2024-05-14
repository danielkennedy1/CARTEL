import click
import requests
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from narco.conf import CARTEL_URL
from narco.crypto import encrypt_file, decrypt
from narco.local import get_state, get_local_keys, update_state, get_state

@click.command(help="Share a file with the cartel")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("to", type=str)
def send(file_path, to):
    sender = get_state()["user"]
    sender_pubkey, sender_privkey = get_local_keys(sender)  # get only sender's private key
    
    verify_pubkey(sender, sender_pubkey)

    receiver = requests.post(f"{CARTEL_URL}/users", json={"name": to})

    if receiver.status_code != 200:
        click.echo(f"Error: {receiver.text}")
        return

    receiver = json.loads(receiver.content.decode("utf-8"))
    receiver_pubkey = RSA.import_key(receiver["public_key"])
    ciphertext = encrypt_file(file_path, receiver_pubkey)

    # sign the message
    hash = SHA256.new(ciphertext)
    signature = pkcs1_15.new(sender_privkey).sign(hash)

    password = click.prompt("Enter your password", hide_input=True)

    sender = get_user_by_name(sender)
    if sender is None:
        click.echo(f"Error: {sender} not found in the cartel")
        return

    sender_user_id = sender["id"]
    receiver_user_id = receiver["id"]

    message = requests.put(
        f"{CARTEL_URL}/messages",
        json={
            "sender": sender_user_id,
            "recipient": receiver_user_id,
            "password": password,
            "message": ciphertext.hex(),
            "signature": signature.hex(),
            "nonce": get_state()["nonce"],
        },
    )

    update_state({"nonce": get_state()["nonce"] + 1})

    if message.status_code != 200:
        click.echo(f"Error: {message.text}")
        return

# verify the public key of a given username in the cartel against the one in the local keys
def verify_pubkey(username: str, local_pubkey: RSA.RsaKey):
    user = get_user_by_name(username)

    if user is None:
        click.echo(f"Error: {username} not found in the cartel")
        return

    # import/export for same format comparison
    remote_pubkey = RSA.import_key(user["public_key"])
    if local_pubkey.export_key() != remote_pubkey.export_key():
        click.echo(f"Error: {username} public key is different from the one in the cartel")
        return

def get_user_by_name(name: str):
    response = requests.post(f"{CARTEL_URL}/users", json={"name": name})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return None
    return response.json()


def get_user_by_id(id: int):
    response = requests.post(f"{CARTEL_URL}/users", json={"id": id})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return None
    return response.json()


@click.command(help="Get details of a user in the cartel")
@click.argument("username", type=str)
def whois(username: str):
    click.echo(get_user_by_name(username))


@click.command(help="List all usernames in the cartel")
def narcos():
    response = requests.get(f"{CARTEL_URL}/users")
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return
    for user in response.json():
        click.echo(user)

#MAYBE: format output, do dont show read ones, include sender info too, etc.
@click.command(help="List my messages")
def inbox():
    if get_state().get("user") is None:
        click.echo(
            "User not selected. Please run `select` to select a user or `init` to create one.")
        return
    my_profile = get_user_by_name(get_state()["user"])
    if my_profile is None:
        return
    user_id = my_profile["id"]
    if user_id is None:
        return
    response = requests.post(
        f"{CARTEL_URL}/messages", json={"user_id": user_id})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return
    for message in response.json():
        click.echo(message)


#MAYBE: require password to read
@click.command(help="Get contents of a message")
@click.argument("message_id", type=int)
def read(message_id: int):
    response = requests.post(
        f"{CARTEL_URL}/messages", json={"message_id": message_id})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return

    response = response.json()

    message_id = response["id"]
    sender_id = response["sender"]
    recipient_id = response["recipient"]
    message_ciphertext = bytes.fromhex(response["message"])
    signature = response["signature"]

    _, private_key = get_local_keys(get_state()["user"])

    sender = get_user_by_id(sender_id)
    if sender is None:
        click.echo("Error: sender not found in the cartel")
        return

    sender_pubkey = RSA.import_key(sender["public_key"])

   # verify the signature
    hash = SHA256.new(message_ciphertext)

    try:
        pkcs1_15.new(sender_pubkey).verify(hash, bytes.fromhex(signature))
        click.echo("Signature is valid")
    except ValueError:
        click.echo("Signature is invalid")
        return

    click.echo(f"Message ID: {message_id}")
    click.echo(f"Sender ID: {sender_id}")
    click.echo(f"Recipient ID: {recipient_id}")

    # decrypt the message
    decrypted = decrypt(message_ciphertext, private_key)

    click.echo("Decrypted message:")
    click.echo(decrypted.decode("utf-8"))
