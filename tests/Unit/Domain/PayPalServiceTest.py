import unittest

from modules.Domain.Services.PayPalService import PayPalService
from modules.Domain.Plugins.PayPalPlugin import PayPalPlugin
from modules.Domain.Plugins.AbstractResponse import AbstractResponse
from modules.Entities import Payment
from modules.Entities.Payer import Payer


class FakeResponse(AbstractResponse):

    def is_refunded(self) -> bool:
        pass

    def capture_id(self) -> str | None:
        pass

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

    # TODO: need to be implemented with mock response examples from PayPal

    def create_order(self, payment: Payment, payer: Payer) -> AbstractResponse:
        return FakeResponse({}, payment)

    def capture_payment_for_order(self, payment: Payment) -> AbstractResponse:
        return FakeResponse({}, payment)

    def refund_captured_payment(self, payment: Payment) -> AbstractResponse:
        return FakeResponse({}, payment)

    def show_order_details(self, payment: Payment) -> AbstractResponse:
        return FakeResponse({}, payment)

    def get_access_token(self) -> AbstractResponse:
        return FakeResponse({}, None)


class PayPalServiceTest(unittest.TestCase):

    def test_pay(self):
        service = PayPalService(FakePayPalPlugin('FAKE_CLIENT_ID', 'FAKE_CLIENT_SECRET'))
        payment = Payment.Payment(
                1000,
                'EUR',
                '1234',
                None,
                'FAKE_RETURN_URL'
        )
        payer = Payer(
                'FAKE_FIRST_NAME',
                'FAKE_LAST_NAME',
                'FAKE_EMAIL',
                'FAKE_ADDRESS_1',
                'FAKE_ADDRESS_2',
                'FAKE_CITY',
                'FAKE_COUNTRY_CODE',
                'FAKE_POST_CODE',
                'FAKE_LANG'
            )
        service.pay(payment, payer)
        self.assertEquals(payment.status, Payment.PaymentStatus.PENDING)
        # TODO: needs more assertions
