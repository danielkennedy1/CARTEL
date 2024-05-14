import click
import requests
from Crypto.PublicKey import RSA

from narco.conf import CARTEL_URL

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

# verify the public key of a given username in the cartel against the one in the local keys
def verify_pubkey(username: str, local_pubkey: RSA.RsaKey):
    user = get_user_by_name(username)

    if user is None:
        click.echo(f"Error: {username} not found in the cartel")
        return

    # import/export for same format comparison
    remote_pubkey = RSA.import_key(user["public_key"])
    if local_pubkey.export_key() != remote_pubkey.export_key():
        click.echo(
            f"Error: {username} public key is different from the one in the cartel"
        )
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


