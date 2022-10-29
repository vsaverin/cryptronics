class CryptronicsBaseException(Exception):
    """Base except which all Cryptronics errors extend"""
    pass


class CryptoApiError(CryptronicsBaseException):
    """
    Occurs when result with {"error" : "detail"}
    from one of available crypto APIs recieved
    """
    pass


class UnknowCryptoError(CryptronicsBaseException):
    """
    Occurs when no errors from crypto APIs recieved
    but still no result are give
    """
    pass
