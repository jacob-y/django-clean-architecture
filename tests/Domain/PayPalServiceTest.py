import unittest

from modules.Domain.Services.PayPalService import PayPalService
from modules.Domain.Plugins.PayPalPlugin import PayPalPlugin
from modules.Domain.Plugins.AbstractResponse import AbstractResponse
from modules.Entities import Payment
from modules.Entities.Payer import Payer


class FakeResponse(AbstractResponse):

    def error_message(self) -> str | None:
        pass

    def error_code(self) -> str | None:
        pass

    def is_successful(self) -> bool:
        pass

    def is_pending(self) -> bool:
        pass

    def redirect_url(self) -> str | None:
        pass

    def id(self) -> str | None:
        pass

    def status(self) -> str | None:
        pass


class FakePayPalPlugin(PayPalPlugin):

    def create_order(self, payment: Payment, payer: Payer) -> AbstractResponse:
        return []

    def capture_payment_for_order(self, payment: Payment) -> AbstractResponse:
        return []

    def refund_captured_payment(self, payment: Payment) -> AbstractResponse:
        return []

    def show_order_details(self, payment: Payment) -> AbstractResponse:
        return []

    def get_access_token(self) -> AbstractResponse:
        return ()


class PayPalServiceTest(unittest.TestCase):

    def test_pay(self):
        service = PayPalService()
