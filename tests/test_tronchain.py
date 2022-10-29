import unittest
from Cryptronics.coins.trx import TronChain


class TronTests(unittest.TestCase):
    def test_init(self):
        trx = TronChain()
        self.assertIs(trx, TronChain)
