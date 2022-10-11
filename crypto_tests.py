import unittest
import random

from Cryptronics.base_crypto import Crypto


class CryptoClassTests(unittest.TestCase):
    def setUp(self) -> None:
        self.crypto = Crypto(
            octopus_api_key='',
            crypto_api_key='',
            eth_api_key='',
            bnb_api_key='',
        )
        return super().setUp()

    # Check if class initialized correctly
    def test_init(self):
        self.assertIsInstance(self.crypto, Crypto)

    # Test OctopusApiSoftware API
    def test_octopus_usdt(self):
        response = self.crypto.create_wallet(
            'usdt', str(random.randrange(1000000, 9000000)))
        print("USDT:", response)
        self.assertIn('result', response.keys(), msg=response)

    # Test CryptoCurrency API
    def test_crypto_btc(self):
        response = self.crypto.create_wallet(
            'btc', str(random.randrange(1000000, 9000000)))
        print("BTC:", response)
        self.assertIn('result', response.keys(), msg=response)

    # Test Eth API
    def test_eth(self):
        response = self.crypto.create_wallet(
            'eth', str(random.randrange(1000000, 9000000)))
        print("ETHER:", response)
        self.assertIn('result', response.keys(), msg=response)

    # Test BNB API
    def test_bnb(self):
        response = self.crypto.create_wallet(
            'bnb', str(random.randrange(1000000, 9000000)))
        print("BNB:", response)
        self.assertIn('result', response.keys(), msg=response)


if __name__ == '__main__':
    unittest.main()
