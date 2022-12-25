# Base dep's
import unittest

# Blockchain dep's
from Cryptronics.coins.trx import TronChain

# Types
from Cryptronics.coins.custom_types import Account


class TronTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trx = TronChain()
        account = self.trx.generate_account()
        self.pr_key = account.private_key
        self.pu_key = account.public_key
        return super().setUp()

    def test_account_generator(self):
        acc = self.trx.generate_account()
        self.assertIsInstance(acc, Account)

    def test_keys_exists(self):
        acc = self.trx.generate_account()
        self.assertIsNotNone(acc.private_key)
        self.assertIsNotNone(acc.public_key)

    def test_get_balance(self):
        balance = self.trx.get_balance(self.pu_key)
        self.assertIsInstance(balance, float)

    def test_get_token_balance(self):
        balance = self.trx.get_token_balance(self.pu_key, 'trx')
        self.assertIsInstance(balance, float)

    def test_send_transaction(self):
        receiver_account = self.trx.generate_account()
        self.trx.send(
            to=receiver_account.public_key,
            amount=1.0,
            private_from=self.pr_key,
            public_from=self.pu_key
        )

    def tearDown(self) -> None:
        return super().tearDown()
