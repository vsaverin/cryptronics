# Base dep's
import requests
from random import randrange
from hashlib import sha256

# Bitcoin dep's
from bitcoin.bci import history
from bitcoin.main import privkey_to_pubkey, privkey_to_address, \
    encode_privkey, decode_privkey
from bit import PrivateKey

# Local dep's
from custom_types import BitcoinAccount


class BitcoinChain(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_account() -> BitcoinAccount:
        private = sha256(
            str(randrange(1, 2**256)).encode('utf-8')
        ).hexdigest()
        public = privkey_to_pubkey(private)
        address = privkey_to_address(private)

        return BitcoinAccount(
            private_key=private,
            public_key=public,
            address=address
        )

    @staticmethod
    def get_transactions_history(
        address: str,
    ) -> list[dict]:
        return history(address)

    @staticmethod
    def satoshi_to_btc(amwount: int):
        return int(amwount)/100000000

    @staticmethod
    def send(
        from_private: str,
        to: str,
        amount: float
    ) -> str:
        account = PrivateKey(wif=encode_privkey(from_private, 'wif'))
        return account.send(
            outputs=[(to, amount, 'btc')]
        )

    @staticmethod
    def mass_send(
        from_private: str,
        to: list[str],
        amount: float
    ) -> str:
        account = PrivateKey(encode_privkey(from_private, 'wif'))
        outputs = [(addr, amount, 'btc') for addr in to]
        return account.send(outputs)

    @staticmethod
    def calculate_balance(
        wallet: str
    ) -> int:
        """Calculate wallet balance from wallet hitstory

        Args:
            history (list[dict]): List of wallet transactions

        Returns:
            int: Wallet now balance in satoshi
        """
        if type(wallet) is not str:
            raise ValueError("wallet should be string")

        BALANCE_URL = 'https://blockchain.info/q/addressbalance/'
        balance_satoshi = int(requests.get(BALANCE_URL + wallet).text)
        return balance_satoshi
