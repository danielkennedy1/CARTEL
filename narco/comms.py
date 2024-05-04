import click
import requests
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from narco.conf import CARTEL_URL
from narco.encrypt import encrypt_file
from narco.local import get_state, get_local_keys

@click.command(help="Share a file with the cartel")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("to", type=str)
def send(file_path, to):
    sender = get_state()["user"]
    _, sender_privkey = get_local_keys(sender)  # get only sender's private key
    ciphertext = encrypt_file(file_path, sender_privkey)
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

    message = requests.put(
        f"{CARTEL_URL}/messages",
        json={
            "sender": sender,
            "recipient": to,
            "message": ciphertext.hex(),
            "signature": signature.hex(),
        },
    )

    if message.status_code != 200:
        click.echo(f"Error: {message.text}")
        return


@click.command(help="Get details of a user in the cartel")
@click.argument("username", type=str)
def whois(username: str):
    response = requests.post(f"{CARTEL_URL}/users", json={"name": username})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return
    click.echo(response.json())

@click.command(help="List all usernames in the cartel")
def narcos():
    response = requests.get(f"{CARTEL_URL}/users")
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return
    for user in response.json():
        click.echo(user)

