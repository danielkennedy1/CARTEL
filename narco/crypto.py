from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad


def encrypt_file(file: str, passkey: bytes) -> bytes:
    cipher = AES.new(passkey, AES.MODE_CBC)
    with open(file, "rb") as file:
        plaintext = file.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return cipher.iv + ciphertext


def decrypt(input: bytes, passkey: bytes) -> bytes:
    iv = input[:16]
    ciphertext = input[16:]
    cipher = AES.new(passkey, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext


def encrypt(input: bytes, key: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(key)

    max_length = key.size_in_bytes() - 42

    encrypted_blocks = []
    for i in range(0, len(input), max_length):
        block = input[i : i + max_length]
        encrypted_blocks.append(cipher.encrypt(block))

    return b"".join(encrypted_blocks)
