# Local dep's
from custom_types import Account

# Litecoin dep's
from litecoinutils.keys import PrivateKey
from litecoinutils.setup import setup
from litecoinutils.proxy import NodeProxy
# from litecoinutils.transactions import Transaction, TxInput, TxOutput


class Litecoin(object):
    def __init__(
        self,
        address: str,
        port: int,
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