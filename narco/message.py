import os
import click
import requests

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

from narco.conf import CARTEL_URL
from narco.crypto import encrypt_file, decrypt
from narco.local import get_state, get_local_keys, update_state
from narco.user import get_user_by_name, verify_pubkey, get_user_by_id


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


@click.command(help="Get contents of a message")
@click.argument("message_id", type=int)
def read(message_id: int):
    response = requests.post(
        f"{CARTEL_URL}/messages", json={"message_id": message_id})
    if response.status_code != 200:
        click.echo(f"Error: {response.text}")
        return

    response = response.json()

    passkey_cipher = PKCS1_OAEP.new(get_local_keys(get_state()["user"])[1])
    passkey = passkey_cipher.decrypt(bytes.fromhex(response["passkey"]))

    sender = get_user_by_id(response["sender"])
    if sender is None:
        click.echo("Error: sender not found in the cartel")
        return

    sender_pubkey = RSA.import_key(sender["public_key"])

    # verify the signature
    hash = SHA256.new(bytes.fromhex(response["message"]))

    try:
        pkcs1_15.new(sender_pubkey).verify(
            hash, bytes.fromhex(response["signature"]))
        click.echo("Signature is valid")
    except ValueError:
        click.echo("Signature is invalid")
        return

    click.echo(f"Message ID: {response['id']}")
    click.echo(f"Sender ID: {response['sender']}")
    click.echo(f"Recipient ID: {response['recipient']}")

    decrypted = decrypt(bytes.fromhex(response["message"]), passkey)

    download_dir_chosen = click.prompt(
        f"Choose location in {os.path.expanduser("~")}/")
    download_dir = os.path.join(os.path.expanduser("~"), download_dir_chosen)
    download_name = click.prompt("Name this file")
    download_path = os.path.join(download_dir, download_name)
    click.echo(f"File saved to {download_path}")

    try:
        with open(download_path, "wb") as download_file:
            download_file.write(decrypted)
    except IOError as e:
        click.echo(f"Failed to write file. {e}")
        click.echo(decrypted)
        return


@click.command(help="Share a file with the cartel")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("to", type=str)
def send(file_path, to):
    sender = get_state()["user"]
    sender_pubkey, sender_privkey = get_local_keys(sender)

    verify_pubkey(sender, sender_pubkey)

    receiver = get_user_by_name(to)

    if receiver is None:
        return

    receiver_pubkey = RSA.import_key(receiver["public_key"])

    password = click.prompt("Enter your password", hide_input=True)

    sender = get_user_by_name(sender)
    if sender is None:
        click.echo(f"Error: {sender} not found in the cartel")
        return

    passkey = get_random_bytes(32)
    passkey_cipher = PKCS1_OAEP.new(receiver_pubkey)
    passkey_ciphertext = passkey_cipher.encrypt(passkey)

    ciphertext = encrypt_file(file_path, passkey)

    hash = SHA256.new(ciphertext)
    signature = pkcs1_15.new(sender_privkey).sign(hash)
    message = requests.put(
        f"{CARTEL_URL}/messages",
        json={
            "sender": sender["id"],
            "recipient": receiver["id"],
            "password": password,
            "message": ciphertext.hex(),
            "signature": signature.hex(),
            "nonce": get_state()["nonce"],
            "passkey": passkey_ciphertext.hex(),
        },
    )

    update_state({"nonce": get_state()["nonce"] + 1})

    if message.status_code != 200:
        click.echo(f"Error: {message.text}")
        return
