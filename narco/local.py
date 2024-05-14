import os
import json
from typing import Tuple
import click
import requests
from Crypto.PublicKey import RSA

from narco.conf import cartel_dir, CARTEL_URL


@click.command(help="Generate your key pairs to access the cartel")
def init():
    try:
        if not os.path.exists(cartel_dir):
            os.mkdir(cartel_dir)

        username = click.prompt("Enter your desired username")
        user_list = requests.get(f"{CARTEL_URL}/users").json()

        if username in user_list:
            click.echo(f"Username {username} already exists")
            return

        key = RSA.generate(3072)

        password = click.prompt("Enter a password", hide_input=True)

        user = requests.put(
            f"{CARTEL_URL}/users",
            json={
                "name": username,
                "public_key": key.publickey().export_key("PEM").decode("utf-8"),
                "password": password,
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

        update_state({"user": username, "nonce": 0})

    except Exception as e:
        click.echo(f"Error: {str(e)}")


@click.command(help="Display the current user")
def whoami():
    click.echo(get_state()["user"])


@click.command(help="Select local user")
def select():
    users = requests.get(f"{CARTEL_URL}/users").json()

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


def get_state() -> dict:
    if not os.path.exists(os.path.join(cartel_dir, "state.json")):
        with open(os.path.join(cartel_dir, "state.json"), "w") as f:
            f.write("{}")
            f.flush()
            f.close()

    with open(os.path.join(cartel_dir, "state.json"), "r") as f:
        result = json.loads(f.read())
        return dict(result)

#NOTE: This function will only change fields that are passed in the state dictionary
def update_state(input_state: dict):
    current_state = get_state()

    new_state = {**current_state, **input_state}

    with open(os.path.join(cartel_dir, "state.json"), "w") as f:
        f.write(json.dumps(new_state))


def get_local_keys(user: str) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    with open(os.path.join(cartel_dir, f"{user}/key.pem"), "rb") as f:
        private_key = RSA.import_key(f.read())
        if private_key is None:
            raise ValueError("Invalid private key")

    with open(os.path.join(cartel_dir, f"{user}/key.pem.pub"), "rb") as f:
        public_key = RSA.import_key(f.read())
        if public_key is None:
            raise ValueError("Invalid public key")

    return public_key, private_key

