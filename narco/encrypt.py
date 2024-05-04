from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def get_key_bytes_length(public_key) -> int:
    key: bytes = public_key.public_key().export_key()
    return len(key[key.index(b"\n") : key.rindex(b"\n")])


def encrypt_file(file: str, key: RSA.RsaKey) -> bytes:
    buffer_size = get_key_bytes_length(key) // 2
    scrambler = PKCS1_OAEP.new(key)
    encrypted_chunks = []

    with open(file, "rb") as f:
        while True:
            to_encrypt = f.read(buffer_size)
            if len(to_encrypt) == 0:
                break

            encrypted = scrambler.encrypt(to_encrypt)
            encrypted_chunks.append(encrypted)

        plaintext = f.read()

    encryptor = PKCS1_OAEP.new(key)
    ciphertext = encryptor.encrypt(plaintext)
    encrypted_chunks.append(ciphertext)
    return b"".join(encrypted_chunks)

