import unittest

from modules.Application.PluginAdaptors.Stripe.StripePluginAdaptor import StripePluginAdaptor
from modules.Domain.Services.StripeService import StripeService
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer
from modules.Entities.Card import Card
from unittest import mock
import stripe


def mocked_stripe_create_payment_method(*args, **kwargs):
    return stripe.convert_to_stripe_object({})


def mocked_stripe_retrieve_payment_method(*args, **kwargs):
    return stripe.convert_to_stripe_object(
        {
            'id': 'pm_1PNvfuEA85d52ktwsL600Hcs',
            'object': 'payment_method',
            'allow_redisplay': 'unspecified',
            'billing_details': {
                "address": {
                    "city": None,
                    "country": None,
                    "line1": None,
                    "line2": None,
                    "postal_code": None,
                    "state": None
                },
                "email": None,
                "name": None,
                "phone": None
            },
            'card': {
                "brand": "visa",
                "checks": {
                    "address_line1_check": None,
                    "address_postal_code_check": None,
                    "cvc_check": "unchecked"
                },
                "country": "US",
                "display_brand": "visa",
                "exp_month": 6,
                "exp_year": 2025,
                "fingerprint": "VgZPkwyreE38RQBo",
                "funding": "credit",
                "generated_from": None,
                "last4": "4242",
                "networks": {
                    "available": [
                        "visa"
                    ],
                    "preferred": None
                },
                "three_d_secure_usage": {
                    "supported": None
                },
                "wallet": None
            },
            'created': 1717501030,
            'customer': None,
            'livemode': False,
            'metadata': {},
            'type': 'card'
        }
    )


def mocked_stripe_create_payment_intent(*args, **kwargs):
    return stripe.convert_to_stripe_object(
        {
            'id': 'pi_3PNvkZEA85d52ktw02jigoks',
            'object': 'payment_intent',
            'amount': 100000,
            'amount_capturable': 0,
            'amount_details': {
                "tip": {}
            },
            'amount_received': 100000,
            'application': None,
            'application_fee_amount': None,
            'automatic_payment_methods': None,
            'canceled_at': None,
            'cancellation_reason': None,
            'capture_method': 'automatic_async',
            'client_secret': 'pi_3PNvkZEA85d52ktw02jigoks_secret_KgaVwLohEbGoa1OUq6pkgWGeY',
            'confirmation_method': 'automatic',
            'created': 1717501319,
            'currency': 'eur',
            'customer': None,
            'description': "0624/1717501317/",
            'invoice': None,
            'last_payment_error': None,
            'latest_charge': 'ch_3PNvkZEA85d52ktw00Udj0rU',
            'livemode': False,
            'metadata': {
                "email": "john.doe@example.com",
                "firstname": "John",
                "lastname": "Doe",
                "number": "1717501317"
            },
            'next_action': None,
            'on_behalf_of': None,
            'payment_method': 'pm_1PNvkYEA85d52ktwakfEh9Pf',
            'payment_method_configuration_details': None,
            'payment_method_options': {
                "card": {
                    "installments": None,
                    "mandate_options": None,
                    "network": None,
                    "request_three_d_secure": "automatic"
                }
            },
            'payment_method_types': ['card'],
            'processing': None,
            'receipt_email': None,
            'review': None,
            'setup_future_usage': None,
            'shipping': None, 'source': None,
            'statement_descriptor': None,
            'statement_descriptor_suffix': 'CARD PAYMENT',
            'status': 'succeeded',
            'transfer_data': None,
            'transfer_group': None
        }
    )


def mocked_stripe_retrieve_payment_intent(*args, **kwargs):
    return stripe.convert_to_stripe_object({})


def mocked_stripe_retrieve_charge(*args, **kwargs):
    return stripe.convert_to_stripe_object(
        {
            'id': 'ch_3PNvkZEA85d52ktw00Udj0rU',
            'object': 'charge',
            'amount': 100000,
            'amount_captured': 100000,
            'amount_refunded': 0,
            'application': None,
            'application_fee': None,
            'application_fee_amount': None,
            'balance_transaction': 'txn_3PNvkZEA85d52ktw0yzGyIJg',
            'billing_details': {
                "address": {
                    "city": None,
                    "country": None,
                    "line1": None,
                    "line2": None,
                    "postal_code": None,
                    "state": None
                },
                "email": None,
                "name": None,
                "phone": None
            },
            'calculated_statement_descriptor': 'STRIPE* CARD PAYMENT',
            'captured': True,
            'created': 1717501320,
            'currency': 'eur',
            'customer': None,
            'description': "0624/1717501317/",
            'destination': None,
            'dispute': None,
            'disputed': False,
            'failure_balance_transaction': None,
            'failure_code': None,
            'failure_message': None,
            'fraud_details': {},
            'invoice': None,
            'livemode': False,
            'metadata': {
                "email": "john.doe@example.com",
                "firstname": "John",
                "lastname": "Doe",
                "number": "1717501317"
            },
            'on_behalf_of': None,
            'order': None,
            'outcome': {
                "network_status": "approved_by_network",
                "reason": None,
                "risk_level": "normal",
                "risk_score": 45,
                "seller_message": "Payment complete.",
                "type": "authorized"
            },
            'paid': True,
            'payment_intent': 'pi_3PNvkZEA85d52ktw02jigoks',
            'payment_method': 'pm_1PNvkYEA85d52ktwakfEh9Pf',
            'payment_method_details': {
                "card": {
                    "amount_authorized": 100000,
                    "brand": "visa",
                    "checks": {
                        "address_line1_check": None,
                        "address_postal_code_check": None,
                        "cvc_check": "pass"
                    },
                    "country": "US",
                    "exp_month": 6,
                    "exp_year": 2025,
                    "extended_authorization": {
                        "status": "disabled"
                    },
                    "fingerprint": "VgZPkwyreE38RQBo",
                    "funding": "credit",
                    "incremental_authorization": {
                        "status": "unavailable"
                    },
                    "installments": None,
                    "last4": "4242",
                    "mandate": None,
                    "multicapture": {
                        "status": "unavailable"
                    },
                    "network": "visa",
                    "network_token": {
                        "used": False
                    },
                    "overcapture": {
                        "maximum_amount_capturable": 100000,
                        "status": "unavailable"
                    },
                    "three_d_secure": None,
                    "wallet": None
                },
                "type": "card"
            },
            'radar_options': {},
            'receipt_email': None,
            'receipt_number': None,
            'receipt_url': 'https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xUEdIMDRFQTg1ZDUya3R3KL_8-7IGMgZJcqfBTCg6LBa7eRGO9zHRSETVeuVEhNH0gU_QlNBHFkXi_P8eucBFN6r_7KOTU2l3ce2s',
            'refunded': False,
            'review': None,
            'shipping': None,
            'source': None,
            'source_transfer': None,
            'statement_descriptor': None,
            'statement_descriptor_suffix': 'CARD PAYMENT',
            'status': 'succeeded',
            'transfer_data': None,
            'transfer_group': None
        }
    )


class StripeAdaptorTest(unittest.TestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        plugin = StripePluginAdaptor('FAKE_SECRET_KEY')
        cls._service = StripeService(plugin)

    @mock.patch('stripe.Charge.retrieve', side_effect=mocked_stripe_retrieve_charge)
    @mock.patch('stripe.PaymentMethod.retrieve', side_effect=mocked_stripe_retrieve_payment_method)
    @mock.patch('stripe.PaymentIntent.create', side_effect=mocked_stripe_create_payment_intent)
    def test_card(self, mocked_create_payment_intent, mocked_retrieve_payment_method, mocked_retrieve_charge):
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
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'succeeded')
        self.assertEqual(payment.gateway_id, 'ch_3PNvkZEA85d52ktw00Udj0rU')
