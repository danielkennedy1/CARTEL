import unittest
import os
from Crypto.Random import get_random_bytes
from narco.crypto import encrypt_file, decrypt_file


class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.shared_secret = get_random_bytes(16)
        self.file_path = "test_file.txt"

        with open(self.file_path, "wb") as f:
            f.write(b"This is some test data")

    def test_encrypt_decrypt_file(self):
        ciphertext = encrypt_file(self.shared_secret, self.file_path)
        decrypted_data = decrypt_file(self.shared_secret, ciphertext)
        self.assertEqual(decrypted_data, b"This is some test data")

    def tearDown(self):
        os.remove(self.file_path)


if __name__ == "__main__":
    unittest.main()
