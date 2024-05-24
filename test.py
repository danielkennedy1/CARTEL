"""

ROUGH IDEA:
    Start server in a separate thread

    Do:
        (dir: root of the project)
        py narco.py init
            alice
            password (could randomly generate)
        py narco.py init 
            bob
            password (could randomly generate)
        py narco.py send README.md alice (or random file)
        py narco.py select
            alice
        py narco.py read 1
            password
            Downloads
            cartel_test_temp_file.txt

        Check:
            README.md content == ~/Downloads/cartel_test_temp_file.txt content
"""

import subprocess
import requests
from time import sleep
import os
import sys
import shutil

from click.testing import CliRunner
from narco.conf import CARTEL_DIR, CARTEL_URL
from narco.local import init, select
from narco.message import send, read

runner = CliRunner()

def clear_cartel_dir():
    for filename in os.listdir(CARTEL_DIR):
        file_path = os.path.join(CARTEL_DIR, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def setup():
    # Nuke the CARTEL_DIR
    clear_cartel_dir()

    # Start the CARTEL
    server = subprocess.Popen([sys.executable, "cartel.py"])

    # Wait for the server to start
    while True:
        try:
            response = requests.get(f"{CARTEL_URL}/users")
            if response.status_code == 200:
                break
        except:
            pass
        sleep(1)

    return server

def init_user(name: str, password: str):
    return runner.invoke(init, input=f"{name}\n{password}")

def send_file(file_path: str, recipient: str, password: str):
    return runner.invoke(send, [file_path, recipient], input=f"{password}\n")

def change_user(name: str):
    return runner.invoke(select, input=f"{name}\n")

def read_file(file_id: int, password: str):
    return runner.invoke(read, [str(file_id)], input=f"{password}\nDownloads\ncartel_test_temp_file.txt")

def main():
    # Given 
    print("Setting up")
    server = setup()

    alice_password = "alicepassword"
    bob_password = "bobpassword"

    # When
    print("Initializing users")

    init_user("alice", alice_password)
    init_user("bob", bob_password)

    print("Sending file")
    send_file("./README.md", "alice", bob_password)

    print("Changing user")
    change_user("alice")

    print("Reading file")
    read_file(1, alice_password)

    # Then
    with open("README.md", "r") as f:
        expected = f.read()

    with open(os.path.join(os.path.expanduser("~"), "Downloads", "cartel_test_temp_file.txt"), "r") as f:
        actual = f.read()

    assert expected == actual

    print("Test passed")

    # Teardown
    server.kill()
    clear_cartel_dir()
    os.remove(os.path.join(os.path.expanduser("~"), "Downloads", "cartel_test_temp_file.txt"))


if __name__ == "__main__":
    main()
