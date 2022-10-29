# Local dep's
from custom_types import Account

# Base dep's
import requests
import json

# Tron dep's
from tronapi import Tron
from tronapi.transactionbuilder import TransactionBuilder
from tronapi.common.transactions import wait_for_transaction_id


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

    def generate_account(self) -> Account:
        account = self.TRON.create_account
        hex = self.TRON.address.to_hex(
            account.address['base58']
        )
        print(hex)
        return Account(
            public_key=account.address['base58'],
            private_key=account.private_key
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