import unittest

from modules.Domain.Services.PayPalService import PayPalService
from modules.Domain.Plugins.AbstractPayPalPlugin import PayPalPlugin
from modules.Entities.Payment import Payment, PaymentMethod, PaymentStatus
from modules.Entities.Payer import Payer
from .FakeResponse import FakeResponse


class FakePayPalPlugin(PayPalPlugin):
    """
      Mock a payment gateway integration.
      """
    def create_order(self, payment: Payment, payer: Payer) -> FakeResponse:
        response = FakeResponse({
            'redirect_url': 'https://fakeurl.com',
            'id': '12345678',
            'status': 'PENDING',
            'is_pending': True
        }, payment)
        response.update_payment()
        return response

    def capture_payment_for_order(self, payment: Payment) -> FakeResponse:
        response = FakeResponse({
            'id': '12345678',
            'capture_id': 'ABCD',
            'status': 'COMPLETED',
            'is_successful': True
        }, payment)
        response.update_payment()
        return response

    def show_order_details(self, payment: Payment) -> FakeResponse:
        response = FakeResponse({
            'id': '12345678',
            'capture_id': 'ABCD',
            'status': 'COMPLETED',
            'is_successful': True
        }, payment)
        response.update_payment()
        return response

    def get_access_token(self) -> FakeResponse:
        return FakeResponse({})


class PayPalServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._service = PayPalService(FakePayPalPlugin('FAKE_CLIENT_ID', 'FAKE_CLIENT_SECRET'))

    def test_pay(self):
        payment = Payment(
                1000,
                'EUR',
                '1234',
                None,
                'FAKE_RETURN_URL',
                PaymentMethod.PAYPAL
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
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        self.assertEqual(payment.gateway_status, 'PENDING')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.redirect_url, 'https://fakeurl.com')

    def test_capture(self):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL',
            payment_method=PaymentMethod.PAYPAL
        )
        self._service.capture(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.capture_id, 'ABCD')

    def test_status(self):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL',
            payment_method=PaymentMethod.PAYPAL
        )
        self._service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '12345678')
        self.assertEqual(payment.capture_id, 'ABCD')
