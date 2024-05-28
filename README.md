# CARTEL

A client-server file sharing CLI application for tamper-detectable, e2e encrypted, and authenticated file sharing.

## Submission

- Adam Byrne (22338004)
- Daniel Kennedy (22340017)

### File structure

| ~ | Description |
| --- | --- |
| `cartel/` | Server-side code |
| cartel.py | Flask server |
| `narco/` | Client-side code |
| narco.py | CLI client |
| test.py | E2E test |
| narco/test_*.py | Client-side tests |
| `docs/` | API & Crypto Documentation |

## Install

```bash
git clone git@github.com:danielkennedy1/CARTEL.git
cd CARTEL

# Install dependencies
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Deploy server

Must be done by a user with sudo privileges (ensure to change user in the `cartel.service` file)

```bash
sudo cp cartel.service /etc/systemd/system/cartel.service
sudo systemctl daemon-reload
sudo systemctl enable cartel.service # Start on boot
sudo systemctl start cartel.service # Start now
```

## Usage

```bash
python cartel.py # Flask Server (uses cartel/ directory)
python narco.py # CLI Client (uses narco/ directory)
```

**Note**:

- A `.cartel` directory will be created in the user's home directory to store local state.

### Commands

```man
python narco.py --help

Usage: narco.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  inbox   List my messages
  init    Generate your key pairs to access the cartel
  narcos  List all usernames in the cartel
  read    Get contents of a message
  select  Select local user
  send    Share a file with the cartel
  whoami  Display the current user
  whois   Get details of a user in the cartel
```

## Testing


## Unit tests

```bash
python -m unittest narco/test_*.py # Run client side tests
python test.py # E2E positive test
```


## Automation
[![E2E Test](https://github.com/danielkennedy1/CARTEL/actions/workflows/e2e_test.yaml/badge.svg)](https://github.com/danielkennedy1/CARTEL/actions/workflows/e2e_test.yaml) [![Python Unit Tests](https://github.com/danielkennedy1/CARTEL/actions/workflows/unit_testing.yaml/badge.svg)](https://github.com/danielkennedy1/CARTEL/actions/workflows/unit_testing.yaml)
Our tests run on GitHub Actions on every push and PR to the main branch. The workflows can be found in `.github/workflows/`.
