import os
import json
from typing import Tuple

import requests
import click
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def encrypt_file(file: str, key: RSA.RsaKey) -> bytes:
    buffer_size = get_key_bytes_length(key) // 2
    scrambler = PKCS1_OAEP.new(key)
    encrypted_chunks = []

    with open(file, "rb") as f:
        while True:
            to_encrypt = f.read(buffer_size)
            if len(to_encrypt) == 0:
                break

            encrypted = scrambler.encrypt(to_encrypt)
            encrypted_chunks.append(encrypted)

        plaintext = f.read()

    encryptor = PKCS1_OAEP.new(key)
    ciphertext = encryptor.encrypt(plaintext)
    encrypted_chunks.append(ciphertext)
    return b"".join(encrypted_chunks)


def get_state():
    cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")
    if not os.path.exists(os.path.join(cartel_dir, "state.json")):
        with open(os.path.join(cartel_dir, "state.json"), "w") as f:
            f.write("{}")

    with open(os.path.join(cartel_dir, "state.json"), "r") as f:
        return json.loads(f.read())


def update_state(state):
    cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")

    with open(os.path.join(cartel_dir, "state.json"), "w") as f:
        f.write(json.dumps(state))


def get_local_keys(user: str) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")
    with open(os.path.join(cartel_dir, f"{user}/key.pem"), "rb") as f:
        private_key = RSA.import_key(f.read())
        if private_key is None:
            raise ValueError("Invalid private key")

    with open(os.path.join(cartel_dir, f"{user}/key.pem.pub"), "rb") as f:
        public_key = RSA.import_key(f.read())
        if public_key is None:
            raise ValueError("Invalid public key")

    return public_key, private_key


def get_key_bytes_length(public_key) -> int:
    key: bytes = public_key.public_key().export_key()
    return len(key[key.index(b"\n") : key.rindex(b"\n")])


@click.group()
def cli():
    pass  # using subcommand pattern


@cli.command(help="Generate your key pairs to access the cartel")
def init():
    try:
        cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")
        if not os.path.exists(cartel_dir):
            os.mkdir(cartel_dir)

        username = click.prompt("Enter your desired username")
        user_list = requests.get("http://127.0.0.1:5000/users").json()

        if username in user_list:
            click.echo(f"Username {username} already exists")
            return

        key = RSA.generate(3072)

        user = requests.put(
            "http://127.0.0.1:5000/users",
            json={
                "name": username,
                "public_key": key.publickey().export_key("PEM").decode("utf-8"),
            },
        )

        if user.status_code != 200:
            click.echo(f"Error: {user.text}")
            return

        # check if username already exists
        if not os.path.exists(os.path.join(cartel_dir, username)):
            os.mkdir(os.path.join(cartel_dir, username))

        with open(os.path.join(cartel_dir, f"{username}/key.pem"), "wb") as f:
            f.write(key.export_key("PEM"))

        with open(os.path.join(cartel_dir, f"{username}/key.pem.pub"), "wb") as f:
            f.write(key.publickey().export_key("PEM"))

        click.echo(
            f"Keys generated and saved at {os.path.abspath(os.path.join(cartel_dir, username))}"
        )

        update_state({"user": username})

    except Exception as e:
        click.echo(f"Error: {str(e)}")


@cli.command(help="Select local user")
def select():
    cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")
    users = requests.get("http://127.0.0.1:5000/users").json()

    for user in users:
        if not os.path.exists(os.path.join(cartel_dir, user)):
            click.echo(f"User {user} does not have keys generated")
            continue

        if not os.path.exists(os.path.join(cartel_dir, user, "key.pem")):
            click.echo(f"User {user} does not have a private key")
            continue

        if not os.path.exists(os.path.join(cartel_dir, user, "key.pem.pub")):
            click.echo(f"User {user} does not have a public key")
            continue

    click.echo("Available users:")
    for user in users:
        click.echo(f" - {user}")

    desired_user = click.prompt("Select a local user")
    update_state({"user": desired_user})


@cli.command(help="Display the current user")
def whoami():
    click.echo(get_state()["user"])


@cli.command(help="Share a file with the cartel")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("to", type=str)
def send(file_path, to):
    sender = get_state()["user"]
    _, sender_privkey = get_local_keys(sender)  # get only sender's private key
    ciphertext = encrypt_file(file_path, sender_privkey)
    receiver = requests.post("http://127.0.0.1:5000/users", json={"name": to})

    if receiver.status_code != 200:
        click.echo(f"Error: {receiver.text}")
        return

    receiver = json.loads(receiver.content.decode("utf-8"))
    receiver_pubkey = RSA.import_key(receiver["public_key"])
    ciphertext = encrypt_file(file_path, receiver_pubkey)

    # sign the message
    h = SHA256.new(ciphertext)
    signature = pkcs1_15.new(sender_privkey).sign(h)

    message = requests.put(
        "http://127.0.0.1:5000/messages",
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

@cli.command(help="List all users in the cartel")
@click.argument("username", type=str)
def whois(username: str):
    response = requests.post("http://127.0.0.1:5000/users", json={"name": username})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return
    click.echo(response.json())

@cli.command(help="List all usernames in the cartel")
def narcos():
    response = requests.get("http://127.0.0.1:5000/users")
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return
    for user in response.json():
        click.echo(user)

if __name__ == "__main__":
    cli()
