# CARTEL

A client-server file sharing CLI application for tamper-detectable, e2e encrypted, and authenticated file sharing.

## Submission

- Adam Byrne (22338004)
- Daniel Kennedy (22340017)

## Documentation
- API Documentation: [API.md](API.md)
- Crypto Documentation: [CRYPTO.md](CRYPTO.md)

## Install

```bash
git clone git@github.com:danielkennedy1/cs4455_FileTransfer.git
cd cs4455_FileTransfer

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

## Notes, Config, and Assumptions

Password hashing is done with Argon2id, using the `argon2_cffi` library. Uses low memory "SECOND RECOMMENDED" configuration from RFC 9106.

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

```bash
python -m unittest narco/test_*.py # Run client side tests
python test.py # E2E positive test
```
