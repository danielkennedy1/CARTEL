import click

from narco.local import init, select, whoami
from narco.user import whois, narcos
from narco.message import send, inbox, read

@click.group()
def cli():
    pass

# Local commands
cli.add_command(init) # Create a new user, generate key pairs
cli.add_command(select) # Select a user from local state
cli.add_command(whoami) # Get the current user name

# Communication commands
cli.add_command(send) # Send a file to the cartel
cli.add_command(whois) # Get details of a user in the cartel
cli.add_command(narcos) # List all usernames in the cartel
cli.add_command(inbox) # List my messages
cli.add_command(read) # Get contents of a message


if __name__ == "__main__":
    cli()
