from decimal import Decimal
import requests
import datetime

from .exceptions import CryptoApiError, UnknowCryptoError
from .crypto_types import MixerWallets, UniqueTags


class Crypto(object):

    def __init__(
        self,
        octopus_api_key: str = None,
        crypto_api_key: str = None,
        eth_api_key: str = None,
        bnb_api_key: str = None,
        mixer_octopus_api_key: str = None,
        mixer_crypto_api_key: str = None,
        mixer_eth_api_key: str = None,
        mixer_bnb_api_key: str = None,
    ) -> None:
        # api keys
        self.OCTOPUS_API_KEY = octopus_api_key
        self.CRYPTO_API_KEY = crypto_api_key
        self.ETH_API_KEY = eth_api_key
        self.BNB_API_KEY = bnb_api_key

        # mixer api keys
        self.MIXER_OCTOPUS_API_KEY = mixer_octopus_api_key
        self.MIXER_CRYPTO_API_KEY = mixer_crypto_api_key
        self.MIXER_ETH_API_KEY = mixer_eth_api_key
        self.MIXER_BNB_API_KEY = mixer_bnb_api_key

        # api url's
        self.OCTOPUS_URL = 'https://tronapi.net/api'
        self.CRYPTO_URL = 'https://cryptocurrencyapi.net/api'
        self.ETH_URL = 'https://etherapi.net/api/v2'
        self.BNB_URL = 'https://bnbapi.net/api'

        # tokens supported
        self.SUPPORTED_TOKENS = {
            'cryptocurrency': ('btc', 'dash', 'doge', 'ltc', 'bch'),
            'octopus':        ('usdt'),
            'ethapi':         ('eth'),
            'bnbapi':         ('bnb')
        }

    def send(
        self,
        token: str,
        to_address: str,
        amount: float,
        tag: str = None,
        mix: bool = False,
        from_address: str = None
    ) -> dict:
        """Send tokens from main address to specified address

        Args:
            token (str): token to send (BTC, ETH etc.)
            to_address (str): address for which tokens need to be sended
            amount (float): amount of tokens to send
            tag (str, optional): to locate operation in API service.
            mix (bool, optional): send coins via mixer
            from_address (str, optional): send from exact address

        Raises:
            TypeError: if token isn't specified
            TypeError: if to_address isn't specified
            TypeError: if amount isn't specified
            TypeError: if token doesn't supported

        Returns:
            dict: response from API service

        """
        if not token:
            raise TypeError("'token' is required argument")
        if not to_address:
            raise TypeError("'to_address' is required argument")
        if not amount:
            raise TypeError("'amount' is required argument")
        if not self.is_token_supported(token):
            raise TypeError(f"Token {token} is not supported")

        key, url, api = self.get_key_and_url(token)
        token = token.upper() if api in ["crypto",
                                         "eth",
                                         "bnb"] else token
        if api == 'crypto':
            cr = f'&currency={token}'
        elif api in ['eth', 'bnb']:
            cr = ''
        else:
            cr = f'&token={token}'
        data = requests.get(
            f'{url}/.send?'
            f'key={key}'
            f'&address={to_address}'
            f'{cr}'
            f'&amount={amount}'
            f'&tag={tag}'
            f'{f"&from={from_address}" if from_address else ""}'
        )
        response = data.json()

        return response

    def create_wallet(
        self,
        token: str,
        tag: str
    ) -> dict:
        """Create new wallet for specified token in blockchain network

        Args:
            token (str): token for which wallet will be created
            tag (str): tag to identify wallet in API service

        Raises:
            TypeError: if token isn't specified

        Returns:
            dict: response from API service
        """
        if not token:
            raise TypeError("'token' is required argument")

        key, url, api = self.get_key_and_url(token)
        if api == 'octopus':
            response = requests.get(
                f'{url}/.give?'
                f'key={key}&'
                f'tag={tag}&'
                f'token={token}'
            )
            return response.json()['result']['address']
        elif api in ('eth', 'bnb'):
            response = requests.get(
                f'{url}/.give?'
                f'key={key}&'
            )
            return response.json()
        elif api in ('cryptocurrency'):
            response = requests.get(
                f'{url}/.give?'
                f'key={key}&'
                f'tag={tag}&'
                f'currency={token.upper()}'
            )
            return response.json()

    def get_key_and_url(
        self,
        token: str
    ) -> list:
        """private function to get key and url for specified token

        Args:
            token (str): token for which url and key will be returned

        Raises:
            TypeError: if tokens isn't specified
            TypeError: if can't find key for this token

        Returns:
            list: api key and api url
        """
        if not token:
            raise TypeError("'token' is required argument")
        key = None

        if token.lower() in self.SUPPORTED_TOKENS['octopus']:
            key, url, api = [self.OCTOPUS_API_KEY, self.OCTOPUS_URL, 'octopus']
        if token.lower() in self.SUPPORTED_TOKENS['cryptocurrency']:
            key, url, api = [self.CRYPTO_API_KEY, self.CRYPTO_URL, 'crypto']
        if token.lower() in self.SUPPORTED_TOKENS['ethapi']:
            key, url, api = [self.ETH_API_KEY, self.ETH_URL, 'eth']
        if token.lower() in self.SUPPORTED_TOKENS['bnbapi']:
            key, url, api = [self.BNB_API_KEY, self.BNB_URL, 'bnb']

        if key:
            return [key, url, api]
        else:
            raise TypeError(f"cannot find api key for token: '{token}'")

    def is_token_supported(
        self,
        token: str
    ) -> bool:
        if not token:
            raise TypeError("'token' is required argument")

        for _, tokens in self.SUPPORTED_TOKENS.items():
            if token in tokens:
                return True

        return False

    def generate_wallets(
        self,
        tokens: list[str],
        tag: str,
    ) -> list:
        """Generate multiple wallets

        Args:
            tokens (list[str]): list of tokens to generate wallets for
            tag (str): unique tag to define wallet in API service.
            For example, it cancontain user id in your database

        Returns:
            list: list of objects
            {
                "wallet":"<wallet_address>",
                "token":"<wallet_token>"
            }
        """
        if not tokens:
            return TypeError("'tokens' is required argument")
        if not tag:
            return TypeError("'tag' is required value")

        wallets = []

        for token in tokens:
            if not self.is_token_supported(token):
                return TypeError(f"Token {token} is not supported")

            wallet = self.create_wallet(token, f"{tag}-{token}")
            try:
                address = wallet.get('result')
            except AttributeError:
                address = wallet
            if address:
                wallets.append(
                    {
                        "wallet": address,
                        "token": token
                    }
                )
            else:
                return {'success': False, 'error': wallet.get('error')}

        return wallets

    def check_transaction(
        self,
        operation_id: str,
        currency: str
    ):
        """Check transaction status on Cryprocurrenct API

        Args:
            operation_id (str): id, returned from send operation
            currency (str): operation currency

        Raises:
            TypeError: if api key not found
            TypeError: if operation_is not provided
            TypeError: if currency not provided

        Returns:
            dict: operation info from API
        """
        if not self.CRYPTO_API_KEY:
            raise TypeError("cryptocurrency api key not found")
        if not operation_id:
            raise TypeError("operation_id is required")
        if not currency:
            raise TypeError("currency is required")
        key, url, name = self.get_key_and_url(currency)
        currency = currency.upper() if name in ["crypto",
                                                "eth",
                                                "bnb"] else currency
        response = requests.get(
            f"{url}/.status?"
            f"key={key}"
            f"&id={operation_id}"
            f"&currency={currency}"
        )
        return response.json()

    def get_balance(
        self,
        currency: str
    ) -> Decimal:
        """Get wallet balance depending on given currency

        Args:
            currency (str): ticker of currency
        Raises:
            AssertionError: if currency is not supported
            CryptoApiError: if errors from crypto APIs recieved
            UnknownCryptoError: if no result in crypto APIs response
        """
        if not self.is_token_supported(currency):
            raise UnknowCryptoError(f'{currency} is not supported')

        key, url, api = self.get_key_and_url(currency)
        currency = currency.upper() if api in ["crypto",
                                               "eth",
                                               "bnb"] else currency
        data = requests.get(
            f'{url}/.balance?'
            f'key={key}'
            f'&{"currency" if api in ["crypto", "eth", "bnb"] else "token"}'
            f'={currency}'
        )
        response = data.json()
        error = response.get("error")

        if error:
            raise CryptoApiError(error)

        if not response.get("result"):
            raise UnknowCryptoError(response)

        return Decimal(response["result"])

    def generate_mixer_wallet_tags(self) -> UniqueTags:
        """Generates unique tags for api's based on timestamp

        Returns:
            UniqueTags: NamedTuple with three unique tags
        """
        return UniqueTags(
            tag_1=f'mixer-{datetime.datetime.now().timestamp()}-1',
            tag_2=f'mixer-{datetime.datetime.now().timestamp()}-2',
            tag_3=f'mixer-{datetime.datetime.now().timestamp()}-3',
        )

    def generate_mixer_wallets(
        self,
        coin: str
    ) -> MixerWallets:
        """Generates new wallets to mix coins

        Args:
            coin (str): sended coin ticker

        Returns:
            MixerWallets: NamedTuple with three new wallets
        """
        tags = self.generate_mixer_wallet_tags()
        return MixerWallets(
            first_wallet=self.create_wallet(
                token=coin,
                tag=tags.tag_1
            ),
            second_wallet=self.create_wallet(
                token=coin,
                tag=tags.tag_2
            ),
            third_wallet=self.create_wallet(
                token=coin,
                tag=tags.tag_3
            )
        )
