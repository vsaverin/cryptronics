from typing import Protocol, Union
from decimal import Decimal


class IDetector(Protocol):

    name: str

    @staticmethod
    def has_injection(string: Union[str, float, int, Decimal]) -> bool:
        ...


class InjectionException(Exception):
    pass


class InjectionDetector:

    _detectors: dict[str, IDetector] = {}

    def __init__(self, query_params: dict):
        self._qp = query_params

    def detect(self, raise_exception: bool = False) -> bool:
        for param in self._qp:
            detector = self._detectors.get(param)
            if detector and detector.has_injection(self._qp[param]):
                if raise_exception:
                    raise InjectionException(f"Injection detected: {detector}")
                return True
        return False
    
    @classmethod
    def register(cls, detector: IDetector):
        cls._detectors[detector.name] = detector


class AddressDetector(IDetector):

    name = "address"

    @staticmethod
    def has_injection(string: str) -> bool:
        return "&" in string or "?" in string or ";" in string


class TokenDetector(AddressDetector):
    
    name = "token"


class CurrencyDetector(AddressDetector):

    name = "currency"


class TagDetector(AddressDetector):

    name = "tag"


class AmountDetector(IDetector):

    name = "amount"

    @staticmethod
    def has_injection(amount: Union[str, float, int, Decimal]) -> bool:
        if isinstance(amount, str):
            try:
                amount = Decimal(amount)
                return False
            except Exception:
                return True
        
        return not (isinstance(amount, int) or isinstance(amount, float) or isinstance(amount, Decimal))


InjectionDetector.register(AddressDetector)
InjectionDetector.register(TokenDetector)
InjectionDetector.register(CurrencyDetector)
InjectionDetector.register(TagDetector)
InjectionDetector.register(AmountDetector)
