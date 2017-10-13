import unittest

from modules.Domain.Services.StripeService import StripeService
from modules.Domain.Plugins.AbstractStripePlugin import StripePlugin
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer
from modules.Entities.Card import Card
from .FakeResponse import FakeResponse


class FakeStripePlugin(StripePlugin):
    """
      Mock a payment gateway integration.
      """
    def create_payment_method(self, payment: Payment, payer: Payer) -> FakeResponse:
        response = FakeResponse({
            'id': '12345678',
            'gateway_id': 'pm_1234',
            'status': 'PENDING',
            'is_pending': True
        }, payment)
        response.update_payment()
        return response

    def create_payment_intent(self, payment: Payment, payer: Payer) -> FakeResponse:
        response = FakeResponse({
            'redirect_url': 'https://fakeurl.com',
            'id': '12345678',
            'status': 'PENDING',
            'gateway_id': 'pi_1234',
            'is_pending': True
        }, payment)
        response.update_payment()
        return response

    def retrieve_payment_method(self, payment: Payment) -> FakeResponse:
        response = FakeResponse({
            'id': '12345678',
            'gateway_id': 'pm_1234',
            'status': 'PENDING',
            'is_pending': True
        }, payment)
        response.update_payment()
        return response

    def retrieve_payment_intent(self, payment: Payment) -> FakeResponse:
        response = FakeResponse({
            'id': '12345678',
            'gateway_id': 'pi_1234',
            'status': 'COMPLETED',
            'is_successful': True
        }, payment)
        response.update_payment()
        return response

    def retrieve_charge(self, payment: Payment) -> FakeResponse:
        response = FakeResponse({
            'id': '12345678',
            'gateway_id': 'ch_1234',
            'status': 'COMPLETED',
            'is_successful': True
        }, payment)
        response.update_payment()
        return response


class StripeServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls._service = StripeService(FakeStripePlugin('FAKE_SECRET_KEY'))

    def test_pay(self):
        payment = Payment(
                1000,
                'EUR',
                '1234',
                None,
                'FAKE_RETURN_URL',
                payment_method=PaymentMethod.CARD,
                card=Card('pm_card_visa', '4242', '12', '25', 'Visa')
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
            'pi_1234',
            'FAKE_RETURN_URL',
            payment_method=PaymentMethod.CARD
        )
        self._service.capture(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '12345678')

    def test_status(self):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            'ch_1234',
            'FAKE_RETURN_URL',
            payment_method=PaymentMethod.CARD
        )
        self._service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '12345678')
