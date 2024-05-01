import os
from typing import Tuple

import click
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


@click.group()
def cli():
    pass


def get_local_keys() -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")
    with open(os.path.join(cartel_dir, "key.pem"), "rb") as f:
        private_key = RSA.import_key(f.read())
        if private_key is None:
            raise ValueError("Invalid private key")

    with open(os.path.join(cartel_dir, "key.pem.pub"), "rb") as f:
        public_key = RSA.import_key(f.read())
        if public_key is None:
            raise ValueError("Invalid public key")

    return public_key, private_key


def get_public_key_bytes_length(public_key) -> int:
    key: bytes = public_key.public_key().export_key()
    return len(key[key.index(b"\n") : key.rindex(b"\n")])


def encrypt_file(file: str, public_key: RSA.RsaKey) -> bytes:
    buffer_size = get_public_key_bytes_length(public_key) // 2
    scrambler = PKCS1_OAEP.new(public_key)

    with open(file, "rb") as f:
        while True:
            to_encrypt = f.read(buffer_size)
            if len(to_encrypt) == 0:
                break

            encrypted = scrambler.encrypt(to_encrypt)
            click.echo(encrypted.hex().encode("utf-8"))

        plaintext = f.read()

        encryptor = PKCS1_OAEP.new(public_key)
        ciphertext = encryptor.encrypt(plaintext)

        return ciphertext


@cli.command(help="Generate your key pairs to access the cartel")
def init():
    try:
        cartel_dir = os.path.join(os.path.expanduser("~"), ".cartel")
        if not os.path.exists(cartel_dir):
            os.mkdir(cartel_dir)

        username = click.prompt("Enter your desired username")
        if not username or len(username) < 3:
            click.echo("Username must be at least 3 characters long")
            return

        key = RSA.generate(3072)

        with open(os.path.join(cartel_dir, "key.pem"), "wb") as f:
            f.write(key.export_key("PEM"))

        with open(os.path.join(cartel_dir, "key.pem.pub"), "wb") as f:
            f.write(key.publickey().export_key("PEM"))

        click.echo(f"Keys generated and saved at {os.path.abspath(cartel_dir)}")

    except Exception as e:
        click.echo(f"Error: {str(e)}")


@cli.command(help="Send a file to the cartel")
@click.argument("file", type=click.Path(exists=True))
@click.argument("to", type=str)
def send(file, to):
    _, privkey = get_local_keys()

    ciphertext = encrypt_file(file, privkey)
    # encrypt with the public key of the recipient


if __name__ == "__main__":
    cli()
