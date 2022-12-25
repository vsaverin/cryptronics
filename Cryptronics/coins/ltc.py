# Local dep's
from custom_types import Account

# Litecoin dep's
# from litecoinutils.constants import SIGHASH_ALL, SIGHASH_NONE,\
#     SIGHASH_SINGLE, SIGHASH_ANYONECANPAY
from litecoinutils.transactions import Transaction, TxInput, TxOutput
from litecoinutils.keys import PrivateKey, P2pkhAddress
from litecoinutils.utils import to_satoshis
from litecoinutils.proxy import NodeProxy
from litecoinutils.script import Script
from litecoinutils.setup import setup


class Litecoin(object):
    def __init__(
        self,
        address: str = None,
        port: int = None,
        username: str = None,
        password: str = None
    ):
        setup('mainnet')
        if address and port and username and password:
            self.PROXY = NodeProxy(
                rpcuser=username,
                rpcpassword=password,
                host=address,
                port=port
            )

    def generate_wallet(self) -> Account:
        priv = PrivateKey()
        pub = priv.get_public_key()
        return Account(
            private_key=priv.to_wif(),
            public_key=pub.get_address().to_string()
        )

    @staticmethod
    def generate_transaction(
        txIn_hash: str,
        to_address: str
    ) -> Transaction:
        tx_in = TxInput(txIn_hash)
        addr = P2pkhAddress(to_address)
        txout = TxOutput(to_satoshis(0.3),
                         Script(['OP_DUP', 'OP_HASH160', addr.to_hash160(),
                                 'OP_EQUALVERIFY', 'OP_CHECKSIG']))
        change_addr = P2pkhAddress('mmYNBho9BWQB2dSniP1NJvnPoj5EVWw89w')
        change_txout = TxOutput(to_satoshis(0.08),
                                Script(['OP_DUP', 'OP_HASH160',
                                        change_addr.to_hash160(),
                                        'OP_EQUALVERIFY', 'OP_CHECKSIG']))
        return Transaction([tx_in], [txout, change_txout])

    def send(
        self,
        to: str,
        amount: str,
        public_from: str,
        private_from: str
    ) -> dict:
        # TODO: Протестировать получение txin и txout адресов
        # из "сырой" транзакции. Проверить с segwit и script операциями.
        return {}
