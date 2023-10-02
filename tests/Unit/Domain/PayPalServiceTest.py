import unittest

from modules.Domain.Services.PayPalService import PayPalService
from modules.Domain.Plugins.AbstractPayPalPlugin import PayPalPlugin
from modules.Domain.Plugins.AbstractResponse import AbstractResponse
from modules.Entities import Payment
from modules.Entities.Payer import Payer


class FakeResponse(AbstractResponse):
    """
    Mock a payment gateway response interpretation.
    """

    def error_message(self) -> str | None:
        return self._data.get('error_message')

    def error_code(self) -> str | None:
        return self._data.get('error_code')

    def is_successful(self) -> bool:
        return self._data.get('is_successful') or False

    def is_pending(self) -> bool:
        return self._data.get('is_pending') or False

    def is_refunded(self) -> bool:
        return self._data.get('is_refunded') or False

    def redirect_url(self) -> str | None:
        return self._data.get('redirect_url')

    def id(self) -> str | None:
        return self._data.get('id')

    def capture_id(self) -> str | None:
        return self._data.get('capture_id')

    def status(self) -> str | None:
        return self._data.get('status')


class FakePayPalPlugin(PayPalPlugin):
    """
      Mock a payment gateway integration.
      """
    def create_order(self, payment: Payment, payer: Payer) -> AbstractResponse:
        response = FakeResponse({
            'redirect_url': 'https://fakeurl.com',
            'id': '12345678',
            'status': 'PENDING',
            'is_pending': True
        }, payment)
        response.update_payment()
        return response

    def capture_payment_for_order(self, payment: Payment) -> AbstractResponse:
        response = FakeResponse({
            'id': '12345678',
            'capture_id': 'ABCD',
            'status': 'COMPLETED',
            'is_successful': True
        }, payment)
        response.update_payment()
        return response

    def refund_captured_payment(self, payment: Payment) -> AbstractResponse:
        response = FakeResponse({
            'id': '12345678',
            'status': 'REFUNDED',
            'is_refunded': True
        }, payment)
        response.update_payment()
        return response

    def show_order_details(self, payment: Payment) -> AbstractResponse:
        response = FakeResponse({
            'id': '12345678',
            'capture_id': 'ABCD',
            'status': 'COMPLETED',
            'is_successful': True
        }, payment)
        response.update_payment()
        return response

    def get_access_token(self) -> AbstractResponse:
        return FakeResponse({})


class PayPalServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._service = PayPalService(FakePayPalPlugin('FAKE_CLIENT_ID', 'FAKE_CLIENT_SECRET'))

    def test_pay(self):
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
        self._service.pay(payment, payer)
        # check that the payment object was correctly updated by the mock payment integrations calls
        self.assertEqual(payment.status, Payment.PaymentStatus.PENDING)
        self.assertEqual(payment.gateway_status, 'PENDING')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.redirect_url, 'https://fakeurl.com')

    def test_capture(self):
        payment = Payment.Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL'
        )
        self._service.capture(payment)
        self.assertEqual(payment.status, Payment.PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.capture_id, 'ABCD')

    def test_status(self):
        payment = Payment.Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL'
        )
        self._service.status(payment)
        self.assertEqual(payment.status, Payment.PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.capture_id, 'ABCD')

    def test_refund(self):
        payment = Payment.Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL'
        )
        self._service.refund(payment)
        self.assertEqual(payment.status, Payment.PaymentStatus.REFUNDED)
        self.assertEqual(payment.gateway_status, 'REFUNDED')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.capture_id, 'ABCD')
