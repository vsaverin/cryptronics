from decouple import config
import unittest

from Cryptronics.mixer import Mixer


class CryptoClassTests(unittest.TestCase):
    def setUp(self) -> None:
        kucoin_api_key = config('main_kucoin_api_key')
        kucoin_secret = config('main_kucoin_secret')
        passphrase = config('main_passphrase')

        self.mixer = Mixer(
            kucoin_api_key=kucoin_api_key,
            kucoin_secret=kucoin_secret,
            passphrase=passphrase,
            outcome_wallets=3,
            is_sandbox=False
        )
        return super().setUp()

    # Trying to get deposit address for BTC
    def test_deposit_wallet(self):
        response = self.mixer.get_deposit_wallet('BTC')
        self.assertIn('address', response.keys(), msg=response)

    # Trying to make market order for BTC-USDT
    def test_market_order(self):
        response = self.mixer.exchange_coin('BTC')
        self.assertIn('orderId', response.keys(), msg=response)


if __name__ == '__main__':
    unittest.main()
