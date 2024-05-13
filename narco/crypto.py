from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_file(shared_secret, file_path):
    cipher = AES.new(shared_secret, AES.MODE_CBC)

    with open(file_path, "rb") as file:
        plaintext = file.read()

    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext, cipher.iv


def decrypt_file(shared_secret, ciphertext, iv):
    cipher = AES.new(shared_secret, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext, AES.block_size)


def file_to_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()
