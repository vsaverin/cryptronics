# Base dep's
from collections import namedtuple
import requests
import json

# Litecoin dep's
from litecoinutils.keys import PrivateKey
from litecoinutils.setup import setup

# Tron dep's
from tronapi import Tron
from tronapi.transactionbuilder import TransactionBuilder
from tronapi.common.transactions import wait_for_transaction_id


class Litecoin(object):
    def __init__(
        self,
        address: str,
        port: int,
        username: str = None,
        password: str = None
    ):
        setup('mainnet')
        # self.PROXY = NodeProxy(
        #     rpcuser=username,
        #     rpcpassword=password,
        #     host=address,
        #     port=port
        # )

    def generate_wallet(self):
        priv = PrivateKey()
        pub = priv.get_public_key()
        return [priv.to_wif(), pub.get_address().to_string()]


class Binance(object):
    pass


class Doge(object):
    pass


class Xmr(object):
    pass


class TronChain(object):
    def __init__(
        self,
        full_node: str = None,
        solidity_node: str = None,
        event_server: str = None
    ):
        """Initial

        Args:
            full_node (str, optional): Full trx node address
            solidity_node (str, optional): Full solidity node address
            event_server (str, optional): Event server address
        """
        self.FULL_NODE = full_node
        self.SOLIDITY_NODE = solidity_node
        self.EVENT_SERVER = event_server
        self.TRON = Tron(
            full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server
        )

    def generate_account(self) -> namedtuple:
        account = self.TRON.create_account
        User = namedtuple('Account', (
            'private',
            'public'
        ))
        hex = self.TRON.address.to_hex(
            account.address['base58']
        )
        print(hex)
        return User(
            public=account.address['base58'],
            private=account.private_key
        )

    def send(
        self,
        to: str,
        amount: float,
        private_from: str,
        public_from: str
    ) -> dict:
        """Send TRX to account

        Args:
            to (str): Payment destination
            amount (float): Amount of TRX
            private_from (str): From wallet private address
            public_from (str): From wallet public address

        Raises:
            TypeError: If amount is not float

        Returns:
            dict: Response from TRON node
        """
        if not isinstance(amount, float):
            raise TypeError('Amount must be type Float')
        self.TRON.private_key = private_from
        self.TRON.default_address = public_from
        builder = TransactionBuilder(self.TRON)
        transaction = builder.send_transaction(to, amount)
        signed_transaction = self.TRON.trx.sign(transaction)
        return self.TRON.trx.broadcast(signed_transaction)

    def get_balance(self, address: str) -> float:
        return self.TRON.trx.get_balance(address, is_float=True)

    @staticmethod
    def get_token_balance(address, ticker):
        url = "https://apilist.tronscan.org/api/account"
        payload = {
            "address": address,
        }
        res = requests.get(url, params=payload)
        balances = json.loads(res.text)["trc20token_balances"]
        data = (item for item in balances if item["symbol"] == ticker)
        token_balance = next(data, None)
        if token_balance is None:
            return 0
        else:
            return int(token_balance["balance"])

    def wait_transaction(self, txid: str):
        return wait_for_transaction_id(self.TRON, txid)

    def from_hex(self, address):
        return self.TRON.address.from_hex(address)


if __name__ == '__main__':
    # ltc = Litecoin(address='127.0.0.1', port=1234)
    # private, public = ltc.generate_wallet()
    # print(f"Private: {private}")
    # print(f"Public: {public}")

    tpr = 'ebd3747067bf9a54f297ec9ad465f74dc91d1144e1500b8c927de44f56dbb327'
    tpu = 'TN5oryHGWRcKpjAw3BY1xTXVhCDy4S9pRW'
    trx = TronChain()

    print(trx.get_balance('TN5oryHGWRcKpjAw3BY1xTXVhCDy4S9pRW'))
    print(trx.get_token_balance('TN5oryHGWRcKpjAw3BY1xTXVhCDy4S9pRW', 'SWH'))

    # account = trx.generate_account()
    # print(account.public)
    # print(account.private)

    # response = trx.send(
    #     to='TGHPsf5eMXgFNiLeuSfueK8xZJWahtYxrY',
    #     amount=1.0,
    #     private_from=tpr,
    #     public_from=tpu
    # )
    # for k, v in response.items():
    #     print(k, v)
