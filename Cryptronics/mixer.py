import requests
import hashlib
import base64
import hmac
import time
import json


class Mixer:
    def __init__(
        self,
        kucoin_api_key: str,
        kucoin_secret: str,
        passphrase: str,
        outcome_wallets: int,
        is_sandbox: bool = False
    ):
        """Init method

        Args:
            kucoin_api_key (str): Public key for your main kucoin account
            kucoin_secret (str): Private key for your main kucoin account
            passphrase (str): Secret passphrase for kucoin account
            outcome_wallets (int): Amount of outcome wallets for mixing
            is_sandbox (bool, optional): Using sandbox API. Defaults to False.

        Raises:
            ConnectionError: If check check failed
        """
        if not passphrase:
            raise TypeError('Passphrase is required')
        if not kucoin_api_key:
            raise TypeError('kucoin_api_key is required')
        if not kucoin_secret:
            raise TypeError('kucoin_secret is required')
        self.API_KEY_VERSION = '2'
        self.IS_SANDBOX = is_sandbox
        self.PASSPHRASE = passphrase
        self.BASE_URL = self._get_api_url()
        if not self._check_connection(kucoin_api_key, kucoin_secret):
            raise ConnectionError('api connection error')
        self.KUCOIN_API_KEY = kucoin_api_key
        self.KUCOIN_SECRET = kucoin_secret
        self.OUTCOME_WALLETS = outcome_wallets

        self.MIX_PAIRS = {
            'BTC': {
                'first': 'BTC-USDT',
                'second': 'USDT-BTC'
            },
            'ETH': {
                'first': 'ETH-USDT',
                'second': 'USDT-ETH'
            },
            'USDT': {
                'first': 'USDT-BTC',
                'second': 'BTC-USDT'
            },
            'LTC': {
                'first': 'LTC-USDT',
                'second': 'USDT-LTC'
            },
            'BNB': {
                'first': 'BNB-USDT',
                'second': 'USDT-BNB'
            },
            'XMR': {
                'first': 'XMR-USDT',
                'second': 'USDT-XMR'
            },
            'DOGE': {
                'first': 'DOGE-USDT',
                'second': 'USDT-DOGE'
            }
        }

    def _get_api_url(self):
        if self.IS_SANDBOX:
            return 'https://openapi-sandbox.kucoin.com'
        else:
            return 'https://api.kucoin.com'

    def _get_api_headers(self, api_key, api_secret, path, method, body=''):
        now = int(time.time() * 1000)
        body = json.dumps(body) if body else ''
        if method == 'get':
            str_to_sign = str(now) + method.upper() + path
        else:
            str_to_sign = str(now) + method.upper() + path + body
        signature = base64.b64encode(
            hmac.new(
                api_secret.encode('utf-8'),
                str_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
        )
        passphrase = base64.b64encode(
            hmac.new(
                api_secret.encode('utf-8'),
                self.PASSPHRASE.encode('utf-8'),
                hashlib.sha256
            ).digest()
        )
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": api_key,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": self.API_KEY_VERSION,
            "Content-Type": "application/json"
        }
        return headers

    def _check_connection(self, api_key, api_secret):
        """Check API connection by geting user account info

        Returns:
            bool: True if connected successfuly
        """
        path = '/api/v1/accounts'
        url = f'{self.BASE_URL}{path}'
        method = 'get'
        response = requests.request(method, url, headers=self._get_api_headers(
            api_key, api_secret, path, method
        ))
        if not response.status_code == 200:
            return False
        else:
            return True

    def _request(self, path, method, data=''):
        url = f'{self.BASE_URL}{path}'
        headers = self._get_api_headers(
            self.KUCOIN_API_KEY,
            self.KUCOIN_SECRET,
            path, method, data
        )
        response = requests.request(
            url=url,
            method=method,
            data=data,
            headers=headers
        )
        return response

    def get_deposit_wallet(self, currency: str):
        """Returns deposit wallet and chain information (TRC20/ERC20 etc...)

        Args:
            currency (str): Currency to get address for

        Returns:
            dict: dict with 'address' and 'chain'
        """
        path = '/api/v1/deposit-addresses'
        response = self._request(path, 'post', {'currency': currency})
        if response.status_code == 200:
            return response.json().get('data')
        else:
            return response.json().get('msg')

    def exchange_coin(self, currency: str):
        path = '/api/v1/orders'
        pairs = self.MIX_PAIRS[currency.upper()]
        response = self._request(path, 'post', {
            'clientOid': '1',
            'side': 'buy',
            'symbol': pairs['first'],
            'type': 'market',
            'tradeType': 'TRADE',
            'size': '0.01'
        })
        return response.json()

    def mixed_send(
        self,
        recieve_wallet: str,
        currency: str,
        amount: str,
        chain: str
    ):
        if not currency.upper() in self.MIX_PAIRS.keys():
            raise ValueError(f'currency {currency} is not supported')
        if not recieve_wallet:
            raise ValueError('receive_wallet is required argument')
        if not amount:
            raise ValueError('amount is required argument')
        self.exchange_coin(currency)
