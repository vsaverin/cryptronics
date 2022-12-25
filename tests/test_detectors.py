import unittest
from decimal import Decimal

from Cryptronics.injection_detector import (AddressDetector, AmountDetector,
                                            CurrencyDetector,
                                            InjectionDetector, TagDetector,
                                            TokenDetector, InjectionException, IDetector)


class AddressDetectorTest(unittest.TestCase):

    _sut = AddressDetector

    def test_has_injection_with_ampersand(self):
        address = "DMr6o9C5qy2E7bWJTe9G2qyQqwrwFGWXCq&amount=0.1&currency=ETH&tag=123456789"

        is_dangerous = self._sut.has_injection(address)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_question_mark(self):
        address = "DMr6o9C5qy2E7bWJTe9G2qyQqwrwFGWXCq?amount=0.1?currency=ETH?tag=123456789"

        is_dangerous = self._sut.has_injection(address)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_space(self):
        address = "DMr6o9C5qy2E7bWJTe9G2qyQqwrwFGWXCq amount=0.1 currency=ETH tag=123456789"

        is_dangerous = self._sut.has_injection(address)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_semicolon(self):
        address = "DMr6o9C5qy2E7bWJTe9G2qyQqwrwFGWXCq;amount=0.1"

        is_dangerous = self._sut.has_injection(address)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_colon(self):
        address = "DMr6o9C5qy2E7bWJTe9G2qyQqwrwFGWXCq:amount=0.1"

        is_dangerous = self._sut.has_injection(address)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_no_injection(self):
        address = "DMr6o9C5qy2E7bWJTe9G2qyQqwrwFGWXCq"

        is_dangerous = self._sut.has_injection(address)

        self.assertFalse(is_dangerous)


class TokenDetectorTest(AddressDetectorTest):

    _sut = TokenDetector


class CurrencyDetectorTest(AddressDetectorTest):

    _sut = CurrencyDetector


class TagDetectorTest(AddressDetectorTest):

    _sut = TagDetector


class AmountDetectorTest(unittest.TestCase):

    _sut = AmountDetector

    def test_has_injection_with_symbol_in_str(self):
        amount = "$0.1"

        is_dangerous = self._sut.has_injection(amount)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_word_in_str(self):
        amount = "one"

        is_dangerous = self._sut.has_injection(amount)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_comma_in_str(self):
        amount = "0,1"

        is_dangerous = self._sut.has_injection(amount)

        self.assertTrue(is_dangerous)

    def test_has_injection_with_no_injection_in_str(self):
        amount = "0.1"

        is_dangerous = self._sut.has_injection(amount)

        self.assertFalse(is_dangerous)

    def test_has_no_injection_in_decimal(self):
        amount = Decimal("0.1")

        is_dangerous = self._sut.has_injection(amount)

        self.assertFalse(is_dangerous)

    def test_has_no_injection_in_float(self):
        amount = 0.1

        is_dangerous = self._sut.has_injection(amount)

        self.assertFalse(is_dangerous)

    def test_has_no_injection_in_int(self):
        amount = 1

        is_dangerous = self._sut.has_injection(amount)

        self.assertFalse(is_dangerous)


class InjectionDetectorTest(unittest.TestCase):

    class MockDetector(IDetector):

            name: str = "mock"

            @staticmethod
            def detect():
                return True

    def test_has_injection(self):
        data = {"address": "DMr6o9?C5qy2E7bWJTe9G2qyQqwrwFGWXCq",
                "amount": "0.1", "currency": "ETH", "tag": "123456789"}

        is_dangerous = InjectionDetector(data).detect()

        self.assertTrue(is_dangerous)

    def test_has_no_injection(self):
        data = {"address": "DMr6o9", "amount": "0.1",
                "currency": "ETH", "tag": "123456789"}

        is_dangerous = InjectionDetector(data).detect()

        self.assertFalse(is_dangerous)

    def test_injection_raises_exception(self):
        data = {"address": "DMr6o9?C5qy2E7bWJTe9G2qyQqwrwFGWXCq",
                "amount": "0.1", "currency": "ETH", "tag": "123456789"}

        with self.assertRaises(InjectionException):
            InjectionDetector(data).detect(raise_exception=True)

    def test_register(self):
        InjectionDetector.register(self.MockDetector)

        self.assertIn(self.MockDetector, InjectionDetector._detectors.values())
