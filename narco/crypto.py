from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def encrypt_file(shared_secret, file_path, encrypted_file_path):
    # Create an AES-256-CBC cipher
    cipher = AES.new(shared_secret, AES.MODE_CBC, iv=get_random_bytes(16))

    # Open the file and encrypt it
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Pad the data to a multiple of the block size (16 bytes for AES)
    from Cryptodome.Util.Padding import pad
    padded_data = pad(file_data, AES.block_size)

    # Encrypt the padded data
    return cipher.encrypt(padded_data)


def derive_shared_secret(sender_private_key, receiver_public_key):
    # Deserialize the server's public key
    server_public_key = RSA.import_key(receiver_public_key)

    # Encrypt a random session key with the server's public key
    session_key = get_random_bytes(32)
    encrypted_session_key = PKCS1_OAEP.new(
        server_public_key).encrypt(session_key)

    # Decrypt the encrypted session key with the client's private key
    decrypted_session_key = PKCS1_OAEP.new(
        sender_private_key).decrypt(encrypted_session_key)

    return decrypted_session_key


def file_to_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


def encrypt(input: bytes, key: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(key)

    max_length = key.size_in_bytes() - 42

    encrypted_blocks = []
    for i in range(0, len(input), max_length):
        block = input[i:i+max_length]
        encrypted_blocks.append(cipher.encrypt(block))

    return b"".join(encrypted_blocks)


def decrypt(input: bytes, key: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(key)

    max_length = key.size_in_bytes()

    decrypted_blocks = []
    for i in range(0, len(input), max_length):
        block = input[i:i+max_length]
        decrypted_blocks.append(cipher.decrypt(block))

    return b"".join(decrypted_blocks)
