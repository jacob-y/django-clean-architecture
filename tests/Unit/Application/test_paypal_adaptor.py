import unittest

from modules.Application.PluginAdaptors.PayPal.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Domain.Services.PayPalService import PayPalService
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer
from unittest import mock


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    match args[0]:
        case 'https://api-m.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N':
            return MockResponse(
                {
                    "id": "4H120426JX758114N",
                    "intent": "CAPTURE",
                    "status": "COMPLETED",
                    "purchase_units": [
                        {
                            "reference_id": "1234",
                            "amount": {
                                "currency_code": "EUR",
                                "value": "10.00"
                            },
                            "payee": {
                                "email_address": "demo-merchant@example.com",
                                "merchant_id": "ABCDEF1234"
                            },
                            "description": "Some payment description",
                            "payments": {
                                "captures": [
                                    {
                                        "id": "2TX70987CY861683L",
                                        "status": "COMPLETED",
                                        "amount": {
                                            "currency_code": "EUR",
                                            "value": "10.00"
                                        },
                                        "final_capture": True,
                                        "seller_protection": {
                                            "status": "ELIGIBLE",
                                            "dispute_categories": [
                                                "ITEM_NOT_RECEIVED",
                                                "UNAUTHORIZED_TRANSACTION"
                                            ]
                                        },
                                        "seller_receivable_breakdown": {
                                            "gross_amount": {
                                                "currency_code": "EUR",
                                                "value": "10.00"
                                            },
                                            "paypal_fee": {
                                                "currency_code": "EUR",
                                                "value": "0.00"
                                            },
                                            "net_amount": {
                                                "currency_code": "EUR",
                                                "value": "0.00"
                                            }
                                        },
                                        "links": [
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L",
                                                "rel": "self",
                                                "method": "GET"
                                            },
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L/refund",
                                                "rel": "refund",
                                                "method": "POST"
                                            },
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N",
                                                "rel": "up",
                                                "method": "GET"
                                            }
                                        ],
                                        "create_time": "2023-10-06T14:19:52Z",
                                        "update_time": "2023-10-06T14:19:52Z"
                                    }
                                ]
                            }
                        }
                    ],
                    "payer": {
                        "name": {
                            "given_name": "John",
                            "surname": "Doe"
                        },
                        "email_address": "demo-customer@example.com",
                        "payer_id": "987YTRE",
                        "address": {
                            "address_line_1": "1 Rue des Roses",
                            "admin_area_2": "Nantes",
                            "postal_code": "44000",
                            "country_code": "FR"
                        }
                    },
                    "create_time": "2023-10-06T14:04:16Z",
                    "update_time": "2023-10-06T14:19:52Z",
                    "links": [
                        {
                            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N",
                            "rel": "self",
                            "method": "GET"
                        }
                    ]
                },
                200
            )
        case _:
            return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    match args[0]:
        case 'https://api-m.sandbox.paypal.com/v1/oauth2/token':
            return MockResponse(
                {
                    "scope": "https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks",
                    "access_token": "ACCESS-TOKEN",
                    "token_type": "Bearer",
                    "app_id": "APP-ID",
                    "expires_in": 32384,
                    "nonce": "NONCE"
                },
                200
            )
        case 'https://api-m.sandbox.paypal.com/v2/checkout/orders':
            return MockResponse(
                {
                    "id": "4H120426JX758114N",
                    "intent": "CAPTURE",
                    "status": "PAYER_ACTION_REQUIRED",
                    "payment_source": {
                        "paypal": {
                            "email_address": "demo-customer@personal.example.com",
                            "name": {
                                "given_name": "John",
                                "surname": "Doe"
                            },
                            "address": {
                                "address_line_1": "1 Rue des roses",
                                "address_line_2": "2nd Floor",
                                "admin_area_2": "Nantes",
                                "postal_code": "44000",
                                "country_code": "FR"
                            }
                        }
                    },
                    "purchase_units": [
                        {
                            "reference_id": "1234",
                            "amount": {
                                "currency_code": "EUR",
                                "value": "10.00",
                                "breakdown": {
                                    "item_total": {
                                        "currency_code": "EUR",
                                        "value": "10.00"
                                    }
                                }
                            },
                            "payee": {
                                "email_address": "demo-merchant@example.com"
                            },
                            "payment_instruction": {
                                "disbursement_mode": "INSTANT"
                            },
                            "description": "Some payment description",
                            "custom_id": "Some payment description",
                            "invoice_id": "1234",
                            "soft_descriptor": "TEST",
                            "items": [
                                {
                                    "name": "Payment",
                                    "unit_amount": {
                                        "currency_code": "EUR",
                                        "value": "10.00"
                                    },
                                    "quantity": "1",
                                    "description": "Some payment description",
                                    "category": "PAYMENT"
                                }
                            ]
                        }
                    ],
                    "payer": {
                        "name": {
                            "given_name": "John",
                            "surname": "Doe"
                        },
                        "email_address": "demo-customer@example.com",
                        "address": {
                            "address_line_1": "1 Rue des Roses",
                            "address_line_2": "2nd Floor",
                            "admin_area_2": "Nantes",
                            "postal_code": "44000",
                            "country_code": "FR"
                        }
                    },
                    "create_time": "2023-07-11T14:26:30Z",
                    "links": [
                        {
                            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N",
                            "rel": "self",
                            "method": "GET"
                        },
                        {
                            "href": "https://www.sandbox.paypal.com/checkoutnow?token=4H120426JX758114N",
                            "rel": "payer-action",
                            "method": "GET"
                        }
                    ]
                },
                200
            )
        case 'https://api-m.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N/capture':
            return MockResponse(
                {
                    "id": "1DS82296EK2660116",
                    "intent": "CAPTURE",
                    "status": "COMPLETED",
                    "payment_source": {
                        "paypal": {
                            "email_address": "demo-customer@example.com",
                            "account_id": "H2HNX5QTLYJZC",
                            "account_status": "VERIFIED",
                            "name": {
                                "given_name": "John",
                                "surname": "Doe"
                            },
                            "address": {
                                "address_line_1": "1 Rue des Roses",
                                "admin_area_2": "Nantes",
                                "postal_code": "44000",
                                "country_code": "FR"
                            }
                        }
                    },
                    "purchase_units": [
                        {
                            "reference_id": "1234",
                            "amount": {
                                "currency_code": "EUR",
                                "value": "10.00",
                                "breakdown": {
                                    "item_total": {
                                        "currency_code": "EUR",
                                        "value": "10.00"
                                    },
                                    "shipping": {
                                        "currency_code": "EUR",
                                        "value": "0.00"
                                    },
                                    "handling": {
                                        "currency_code": "EUR",
                                        "value": "0.00"
                                    },
                                    "insurance": {
                                        "currency_code": "EUR",
                                        "value": "0.00"
                                    },
                                    "shipping_discount": {
                                        "currency_code": "EUR",
                                        "value": "0.00"
                                    }
                                }
                            },
                            "payee": {
                                "email_address": "demo-merchant@example.com",
                                "merchant_id": "ABCDEF1234"
                            },
                            "payment_instruction": {"disbursement_mode": "INSTANT"},
                            "description": "Some payment description",
                            "custom_id": "Some payment description",
                            "invoice_id": "1234",
                            "items": [
                                {
                                    "name": "Payment",
                                    "unit_amount": {
                                        "currency_code": "EUR",
                                        "value": "10.00"
                                    },
                                    "tax": {
                                        "currency_code": "EUR",
                                        "value": "0.00"
                                    },
                                    "quantity": "1",
                                    "description": "Payment",
                                    "image_url": ""
                                }
                            ],
                            "shipping": {
                                "name": {"full_name": "John Doe"},
                            },
                            "payments": {
                                "captures": [
                                    {
                                        "id": "2TX70987CY861683L",
                                        "status": "COMPLETED",
                                        "amount": {
                                            "currency_code": "EUR",
                                            "value": "10.00"
                                        },
                                        "final_capture": True,
                                        "disbursement_mode": "INSTANT",
                                        "seller_protection": {"status": "NOT_ELIGIBLE"},
                                        "seller_receivable_breakdown": {
                                            "gross_amount": {
                                                "currency_code": "EUR",
                                                "value": "10.00"
                                            },
                                            "paypal_fee": {
                                                "currency_code": "EUR",
                                                "value": "0.00"
                                            },
                                            "net_amount": {
                                                "currency_code": "EUR",
                                                "value": "0.00"
                                            }
                                        },
                                        "invoice_id": "Some payment description",
                                        "custom_id": "Some payment description",
                                        "links": [
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L",
                                                "rel": "self",
                                                "method": "GET"
                                            },
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L/refund",
                                                "rel": "refund",
                                                "method": "POST"
                                            },
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N",
                                                "rel": "up",
                                                "method": "GET"
                                            }
                                        ],
                                        "create_time": "2023-07-12T15:15:24Z",
                                        "update_time": "2023-07-12T15:15:24Z"
                                    }
                                ]
                            }
                        }
                    ],
                    "payer": {
                        "name": {
                            "given_name": "John",
                            "surname": "Doe"
                        },
                        "email_address": "demo-customer@example.com",
                        "payer_id": "789YTRE",
                        "address": {
                            "address_line_1": "1 Rue des Roses",
                            "admin_area_2": "Nantes",
                            "postal_code": "44000",
                            "country_code": "FR"
                        }
                    },
                    "create_time": "2023-07-12T15:14:17Z",
                    "update_time": "2023-07-12T15:15:24Z",
                    "links": [
                        {
                            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N",
                            "rel": "self",
                            "method": "GET"
                        }
                    ]
                },
                200
            )
        case 'https://api-m.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L/refund':
            return MockResponse(
                {
                    "id": "52V51802J2543164M",
                    "amount":
                        {
                            "currency_code": "EUR",
                            "value": "1.00"
                         },
                    "seller_payable_breakdown": {
                        "gross_amount": {
                            "currency_code": "EUR",
                            "value": "1.00"
                        },
                        "paypal_fee": {
                            "currency_code": "EUR",
                            "value": "0.05"
                        },
                        "net_amount": {
                            "currency_code": "EUR",
                            "value": "0.95"
                        },
                        "total_refunded_amount": {
                            "currency_code": "EUR",
                            "value": "1.00"
                        }
                    },
                    "invoice_id": "TST2621100616040887",
                    "status": "COMPLETED",
                    "create_time": "2021-10-06T07:31:16-07:00",
                    "update_time": "2021-10-06T07:31:16-07:00",
                    "links": [
                        {
                            "href": "https://api.sandbox.paypal.com/v2/payments/refunds/52V51802J2543164M",
                            "rel": "self",
                            "method": "GET"
                        },
                        {
                            "href": "https://api.sandbox.paypal.com/v2/payments/captures/2DW1411898692761B",
                            "rel": "up",
                            "method": "GET"
                        }
                    ]
                },
                200
            )
        case _:
            return MockResponse(None, 404)


class PayPalAdaptorTest(unittest.TestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        plugin = PayPalPluginAdaptor('FAKE_CLIENT_ID', 'FAKE_CLIENT_SECRET')
        cls._service = PayPalService(plugin)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_create(self, mock_post):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            None,
            'FAKE_RETURN_URL',
            payment_method=PaymentMethod.PAYPAL
        )
        payer = Payer(
            'John',
            'Doe',
            'demo-customer@example.com',
            '1 Rue des Roses',
            '2nd Floor',
            'Nantes',
            'FR',
            '44230',
            'fr'
        )
        self._service.pay(payment, payer)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        self.assertEqual(payment.gateway_status, 'PAYER_ACTION_REQUIRED')
        self.assertEqual(payment.gateway_id, '4H120426JX758114N')
        self.assertIn(
            'https://api-m.sandbox.paypal.com/v1/oauth2/token',
            mock_post.call_args_list[0].args[0]
        )
        self.assertIn(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders',
            mock_post.call_args_list[1].args[0]
        )

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_capture(self, mock_get, mock_post):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            '4H120426JX758114N',
            payment_method=PaymentMethod.PAYPAL
        )
        self._service.capture(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '4H120426JX758114N')
        self.assertIn(
            'https://api-m.sandbox.paypal.com/v1/oauth2/token',
            mock_post.call_args_list[0].args[0]
        )
        self.assertIn(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N',
            mock_get.call_args_list[0].args[0]
        )

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_status(self, mock_get, mock_post):
        payment = Payment(
            1000,
            'EUR',
            '1234',
            '4H120426JX758114N',
            payment_method=PaymentMethod.PAYPAL
        )
        self._service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '4H120426JX758114N')
        self.assertIn(
            'https://api-m.sandbox.paypal.com/v1/oauth2/token',
            mock_post.call_args_list[0].args[0]
        )
        self.assertIn(
            'https://api-m.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N',
            mock_get.call_args_list[0].args[0]
        )
