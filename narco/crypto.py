from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def encrypt_file(file: str, key: RSA.RsaKey) -> bytes:
    file_bytes = file_to_bytes(file)
    return encrypt(file_bytes, key)

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
