# Monero dep's
from monero.wallet import Wallet, JSONRPCWallet
from monero.daemon import Daemon, JSONRPCDaemon
# from monero.transaction import Transaction


class MoneroChain(object):
    def __init__(
        self,
        d_host: str = '127.0.0.1',
        d_port: int = 28081,
        d_user: str = None,
        d_password: str = None,
        w_host: str = '127.0.0.1',
        w_port: int = 28081,
        w_user: str = None,
        w_password: str = None,
        only_wallet: bool = True
    ) -> None:
        if not only_wallet:
            self.daemon = Daemon(JSONRPCDaemon(port=d_port))
        self.wallet = Wallet(JSONRPCWallet(port=w_port))

    def send(
        self,
        from_address,
        to_address
    ) -> dict:
        pass
