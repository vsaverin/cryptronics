from typing import NamedTuple


class Account(NamedTuple):
    public_key: str
    private_key: str


class BitcoinAccount(NamedTuple):
    public_key: str
    private_key: str
    address: str
