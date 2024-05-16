import unittest
from narco.crypto import encrypt_file, decrypt


class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.passkey = b"thisisapasskey123456789101112131"
        self.file = "test.txt"

        with open(self.file, "w") as f:
            f.write("test")

    def tearDown(self):
        import os

        os.remove(self.file)

    def test_correctness(self):
        assert decrypt(encrypt_file(self.file, self.passkey), self.passkey) == b"test"


if __name__ == "__main__":
    unittest.main()
