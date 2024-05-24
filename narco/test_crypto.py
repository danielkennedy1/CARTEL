import unittest
from narco.crypto import encrypt_file, decrypt
from Crypto.Random import get_random_bytes


class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.passkey = get_random_bytes(32)
        self.file = "test.txt"

        with open(self.file, "w") as f:
            f.write("test")

    def tearDown(self):
        import os

        os.remove(self.file)

    def test_correctness(self):
        ciphertext, nonce, tag = encrypt_file(self.file, self.passkey)
        assert decrypt(ciphertext, self.passkey, nonce, tag) == b"test"


if __name__ == "__main__":
    unittest.main()
