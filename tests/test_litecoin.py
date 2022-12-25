# Base dep's
import unittest

# Blockchain dep's
from Cryptronics.coins.ltc import Litecoin

# Types
from Cryptronics.coins.custom_types import Account


class LitecoinTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ltc = Litecoin()
        return super().setUp()

    def test_account_generator(self):
        acc = self.ltc.generate_wallet()
        self.assertIsInstance(acc, Account)

    def test_keys(self):
        acc = self.ltc.generate_wallet()
        self.assertIsNotNone(acc.private_key)
        self.assertIsNotNone(acc.public_key)

    def tearDown(self) -> None:
        return super().tearDown()
