from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_file(file: str, passkey: bytes) -> bytes:
    cipher = AES.new(passkey, AES.MODE_CBC)

    with open(file, "rb") as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = bytearray(cipher.iv)

    return bytes(iv + ciphertext)

def decrypt(input: bytes, passkey: bytes) -> bytes:
    iv = input[:16]
    ciphertext = input[16:]

    cipher = AES.new(passkey, AES.MODE_CBC, iv=iv)
    decrypted = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted, AES.block_size)

    return plaintext
