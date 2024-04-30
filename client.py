import click
import rsa

import os
import errno


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--out",
    type=click.Path(),
    default="key.pem",
    help="File path to save the generated keys",
)
def generate_keypair(out):

    try:
        if os.path.exists(out) or os.path.exists(out + ".pub"):
            raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), out)

        (pubkey, privkey) = rsa.newkeys(512)

        with open(out, "wb") as f:
            f.write(privkey.save_pkcs1())

        with open(out + ".pub", "wb") as f:
            f.write(pubkey.save_pkcs1())

        click.echo(f"Keys generated and saved at {out} and {out}.pub")
    except Exception as e:
        if e.errno == errno.EEXIST:
            click.echo(f"Error: Key '{out}' already exists.")
        elif e.errno == errno.EACCES:
            click.echo(f"Error: Permission denied to write to '{out}'.")
        else:
            click.echo(f"Error: {e.strerror}")


if __name__ == "__main__":
    cli()
