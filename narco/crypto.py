from Crypto.Cipher import AES

def encrypt_file(file: str, passkey: bytes):
    with open(file, "rb") as f:
        plaintext = f.read()

    return encrypt(plaintext, passkey)


def encrypt(plaintext: bytes, passkey: bytes):
    cipher = AES.new(passkey, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    return bytes(ciphertext), cipher.nonce, tag

def decrypt(ciphertext: bytes, passkey: bytes, nonce: bytes, tag: bytes) -> bytes:
    cipher = AES.new(passkey, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return plaintext
