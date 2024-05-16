import os
import json
import unittest
from unittest.mock import patch, mock_open
from Crypto.PublicKey import RSA
from narco.local import get_state, update_state, get_local_keys
from narco.conf import CARTEL_DIR


class TestGetState(unittest.TestCase):
    @patch("narco.local.os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_get_state_existing_file(self, mock_open_func, mock_path_exists):
        state = get_state()
        self.assertIsInstance(state, dict)
        self.assertEqual(state, {})

    @patch("narco.local.os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_get_state_non_existing_file(self, mock_open_func, mock_path_exists):
        state = get_state()
        self.assertIsInstance(state, dict)
        self.assertEqual(state, {})


class TestUpdateState(unittest.TestCase):

    @patch("narco.local.get_state", return_value={})
    @patch("builtins.open", new_callable=mock_open)
    def test_update_state(self, mock_open_func, mock_get_state):
        input_state = {"key1": "value1", "key2": "value2"}
        update_state(input_state)
        mock_open_func.assert_called_once_with(
            os.path.join(CARTEL_DIR, "state.json"), "w"
        )
        handle = mock_open_func()
        handle.write.assert_called_once_with(json.dumps(input_state))


class TestGetLocalKeys(unittest.TestCase):
    def setUp(self):
        self.user = "test_user"

        if not os.path.exists(CARTEL_DIR):
            os.mkdir(CARTEL_DIR)

        if not os.path.exists(os.path.join(CARTEL_DIR, self.user)):
            os.mkdir(os.path.join(CARTEL_DIR, self.user))

        self.private_key_path = os.path.join(CARTEL_DIR, self.user, "key.pem")
        self.public_key_path = os.path.join(CARTEL_DIR, self.user, "key.pem.pub")

        key = RSA.generate(2048)
        with open(self.private_key_path, "wb") as f:
            f.write(key.export_key())
        with open(self.public_key_path, "wb") as f:
            f.write(key.publickey().export_key())

    def test_get_local_keys(self):
        private_key, public_key = get_local_keys(self.user)
        self.assertIsInstance(private_key, RSA.RsaKey)
        self.assertIsInstance(public_key, RSA.RsaKey)

    def tearDown(self):
        os.remove(self.private_key_path)
        os.remove(self.public_key_path)


if __name__ == "__main__":
    unittest.main()
