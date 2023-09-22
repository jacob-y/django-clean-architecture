import unittest

from modules.Application.PluginAdaptors.Stripe.StripePluginAdaptor import StripePluginAdaptor
from modules.Domain.Services.StripeService import StripeService
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer
from unittest import mock
import stripe


def mocked_stripe_create_payment_method(*args):
    return stripe.convert_to_stripe_object({})


def mocked_stripe_retrieve_payment_method(*args):
    return stripe.convert_to_stripe_object({})


def mocked_stripe_create_payment_intent(*args):
    return stripe.convert_to_stripe_object({})


def mocked_stripe_retrieve_payment_intent(*args):
    return stripe.convert_to_stripe_object({})


def mocked_stripe_retrieve_charge(*args):
    return stripe.convert_to_stripe_object({})


class StripeAdaptorTest(unittest.TestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        plugin = StripePluginAdaptor('FAKE_SECRET_KEY')
        cls._service = StripeService(plugin)

    @mock.patch('stripe.PaymentMethod.retrieve', side_effect=mocked_stripe_retrieve_payment_method)
    @mock.patch('stripe.PaymentIntent.create', side_effect=mocked_stripe_create_payment_intent)
    def test_pay(self, mocked_create_payment_intent, mocked_retrieve_payment_method):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL',
            payment_method=PaymentMethod.CARD
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
        self.assertEqual(payment.gateway_status, 'PAYER_ACTION_REQUIRED')
        self.assertEqual(payment.gateway_id, '4H120426JX758114N')
#
#    @mock.patch('StripeClient', side_effect=mocked_stripe)
#    def test_capture(self):
#        payment = Payment(
#            1000,
#            'EUR',
#            '1234',
#            '1DS82296EK2660116',
#        )
#        self._service.capture(payment)
#        # check that the payment object was correctly updated by the mock payment integrations calls
#        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
#        self.assertEqual(payment.gateway_status, 'COMPLETED')
#        self.assertEqual(payment.gateway_id, '1DS82296EK2660116')
#
#    @mock.patch('StripeClient', side_effect=mocked_stripe)
#    def test_status(self):
#        payment = Payment(
#            1000,
#            'EUR',
#            '1234',
#            '33889979KA672323F',
#        )
#        self._service.status(payment)
#        # check that the payment object was correctly updated by the mock payment integrations calls
#        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
#        self.assertEqual(payment.gateway_status, 'COMPLETED')
#        self.assertEqual(payment.gateway_id, '33889979KA672323F')
#