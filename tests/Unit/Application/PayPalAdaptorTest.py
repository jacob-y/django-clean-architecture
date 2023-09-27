import unittest
from abc import ABC

from modules.Application.PluginAdaptors.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Application.PluginAdaptors.HTTPClientInterface import HTTPClientInterface
from modules.Domain.Services.PayPalService import PayPalService
from modules.Entities.Payment import Payment, PaymentStatus
from modules.Entities.Payer import Payer
import json


class FakeHTTPClient(HTTPClientInterface, ABC):
    data: list

    def get(self, endpoint: str, headers: dict, auth: tuple) -> dict:
        return json.loads(self.data.pop(0))

    def post(self, endpoint: str, headers: dict, is_form_encoded: bool, data: dict, auth: tuple) -> dict:
        return json.loads(self.data.pop(0))


class PayPalAdaptorTest(unittest.TestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        fake_http_client = FakeHTTPClient()
        plugin = PayPalPluginAdaptor('FAKE_CLIENT_ID', 'FAKE_CLIENT_SECRET', fake_http_client)
        cls._fake_http_client = fake_http_client
        cls._service = PayPalService(plugin)

    def test_pay(self):
        self._fake_http_client.data = [
            '{"scope":"https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks","access_token":"A21AAKRdHNBqKUbNWaLt11sn0Too21Y42GpMif5_dMjvXAdjlLjuPv1mvKpSdaGvCs2rofTsAMKo_VFpyYMh1YNINHmGyG0sg","token_type":"Bearer","app_id":"APP-80W284485P519543T","expires_in":32384,"nonce":"2021-10-06T14:02:50Z52w3KxZIG9RFpjQaWMvj4oiL6mGaxR4-YEqzpNVQ6jE"}',
            '{"id":"4H120426JX758114N","intent":"CAPTURE","status":"PAYER_ACTION_REQUIRED","payment_source":{"paypal":{"email_address":"clarkkent@iraiser.eu","name":{"given_name":"Clark","surname":"Kent"},"address":{"address_line_1":"199 Route de Clisson","address_line_2":"2nd Floor","admin_area_2":"Saint-Sébastien-sur-Loire","postal_code":"44230","country_code":"FR"}}},"purchase_units":[{"reference_id":"TST-1689085589998","amount":{"currency_code":"EUR","value":"10.49","breakdown":{"item_total":{"currency_code":"EUR","value":"10.49"}}},"payee":{"email_address":"dev-facilitator@iraiser.eu"},"payment_instruction":{"disbursement_mode":"INSTANT"},"description":"0711/TST-1689085589998/12345678/","custom_id":"0711/TST-1689085589998/12345678/","invoice_id":"TST-1689085589998","soft_descriptor":"TESTFACILIT","items":[{"name":"Donation","unit_amount":{"currency_code":"EUR","value":"10.49"},"quantity":"1","description":"0711/TST-1689085589998/12345678/","category":"DONATION"}]}],"payer":{"name":{"given_name":"Clark","surname":"Kent"},"email_address":"clarkkent@iraiser.eu","address":{"address_line_1":"199 Route de Clisson","address_line_2":"2nd Floor","admin_area_2":"Saint-Sébastien-sur-Loire","postal_code":"44230","country_code":"FR"}},"create_time":"2023-07-11T14:26:30Z","links":[{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/4H120426JX758114N","rel":"self","method":"GET"},{"href":"https://www.sandbox.paypal.com/checkoutnow?token=4H120426JX758114N","rel":"payer-action","method":"GET"}]}',
        ]
        payment = Payment(
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
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        self.assertEqual(payment.gateway_status, 'PAYER_ACTION_REQUIRED')
        self.assertEqual(payment.gateway_id, '4H120426JX758114N')

    def test_capture(self):
        self._fake_http_client.data = [
            '{"scope":"https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks","access_token":"A21AAKRdHNBqKUbNWaLt11sn0Too21Y42GpMif5_dMjvXAdjlLjuPv1mvKpSdaGvCs2rofTsAMKo_VFpyYMh1YNINHmGyG0sg","token_type":"Bearer","app_id":"APP-80W284485P519543T","expires_in":32384,"nonce":"2021-10-06T14:02:50Z52w3KxZIG9RFpjQaWMvj4oiL6mGaxR4-YEqzpNVQ6jE"}',
            '{"id":"1DS82296EK2660116","intent":"CAPTURE","status":"COMPLETED","payment_source":{"paypal":{"email_address":"yjacob+paypal@iraiser.eu","account_id":"H2HNX5QTLYJZC","account_status":"VERIFIED","name":{"given_name":"yann","surname":"jacob"},"address":{"address_line_1":"199 route de clisson","admin_area_2":"saint sebastien sur loire","postal_code":"44230","country_code":"DE"}}},"purchase_units":[{"reference_id":"LDEV230712-1714-0013","amount":{"currency_code":"EUR","value":"41.00","breakdown":{"item_total":{"currency_code":"EUR","value":"41.00"},"shipping":{"currency_code":"EUR","value":"0.00"},"handling":{"currency_code":"EUR","value":"0.00"},"insurance":{"currency_code":"EUR","value":"0.00"},"shipping_discount":{"currency_code":"EUR","value":"0.00"}}},"payee":{"email_address":"dev-facilitator@iraiser.eu","merchant_id":"6LCX48AYE8CJW"},"payment_instruction":{"disbursement_mode":"INSTANT"},"description":"Don de test","custom_id":"0712/LDEV230712-1714-0013/12/","invoice_id":"LDEV230712-1714-0013","items":[{"name":"Donation","unit_amount":{"currency_code":"EUR","value":"41.00"},"tax":{"currency_code":"EUR","value":"0.00"},"quantity":"1","description":"Don de test","image_url":""}],"shipping":{"name":{"full_name":"yann jacob"}},"payments":{"captures":[{"id":"2TX70987CY861683L","status":"COMPLETED","amount":{"currency_code":"EUR","value":"41.00"},"final_capture":true,"disbursement_mode":"INSTANT","seller_protection":{"status":"NOT_ELIGIBLE"},"seller_receivable_breakdown":{"gross_amount":{"currency_code":"EUR","value":"41.00"},"paypal_fee":{"currency_code":"EUR","value":"2.19"},"net_amount":{"currency_code":"EUR","value":"38.81"}},"invoice_id":"LDEV230712-1714-0013","custom_id":"0712/LDEV230712-1714-0013/12/","links":[{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2TX70987CY861683L/refund","rel":"refund","method":"POST"},{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/1DS82296EK2660116","rel":"up","method":"GET"}],"create_time":"2023-07-12T15:15:24Z","update_time":"2023-07-12T15:15:24Z"}]}}],"payer":{"name":{"given_name":"yann","surname":"jacob"},"email_address":"yjacob+paypal@iraiser.eu","payer_id":"H2HNX5QTLYJZC","address":{"address_line_1":"199 route de clisson","admin_area_2":"saint sebastien sur loire","postal_code":"44230","country_code":"DE"}},"create_time":"2023-07-12T15:14:17Z","update_time":"2023-07-12T15:15:24Z","links":[{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/1DS82296EK2660116","rel":"self","method":"GET"}]}',
        ]
        payment = Payment(
            1000,
            'EUR',
            '1234',
            '1DS82296EK2660116',
        )
        self._service.capture(payment)
        # check that the payment object was correctly updated by the mock payment integrations calls
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '1DS82296EK2660116')

    def test_status(self):
        self._fake_http_client.data = [
            '{"scope":"https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks","access_token":"A21AAKRdHNBqKUbNWaLt11sn0Too21Y42GpMif5_dMjvXAdjlLjuPv1mvKpSdaGvCs2rofTsAMKo_VFpyYMh1YNINHmGyG0sg","token_type":"Bearer","app_id":"APP-80W284485P519543T","expires_in":32384,"nonce":"2021-10-06T14:02:50Z52w3KxZIG9RFpjQaWMvj4oiL6mGaxR4-YEqzpNVQ6jE"}',
            '{"id":"33889979KA672323F","intent":"CAPTURE","status":"COMPLETED","purchase_units":[{"reference_id":"TST2621100616040887","amount":{"currency_code":"EUR","value":"1.00"},"payee":{"email_address":"dev-facilitator@iraiser.eu","merchant_id":"6LCX48AYE8CJW"},"description":"1006/TST2621100616040887/2/","payments":{"captures":[{"id":"2DW1411898692761B","status":"COMPLETED","amount":{"currency_code":"EUR","value":"1.00"},"final_capture":true,"seller_protection":{"status":"ELIGIBLE","dispute_categories":["ITEM_NOT_RECEIVED","UNAUTHORIZED_TRANSACTION"]},"seller_receivable_breakdown":{"gross_amount":{"currency_code":"EUR","value":"1.00"},"paypal_fee":{"currency_code":"EUR","value":"0.44"},"net_amount":{"currency_code":"EUR","value":"0.56"}},"links":[{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2DW1411898692761B","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2DW1411898692761B/refund","rel":"refund","method":"POST"},{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/33889979KA672323F","rel":"up","method":"GET"}],"create_time":"2021-10-06T14:19:52Z","update_time":"2021-10-06T14:19:52Z"}]}}],"payer":{"name":{"given_name":"yann","surname":"jacob"},"email_address":"yjacob+paypal@iraiser.eu","payer_id":"H2HNX5QTLYJZC","address":{"address_line_1":"199 route de clisson","admin_area_2":"saint sebastien sur loire","postal_code":"44230","country_code":"FR"}},"create_time":"2021-10-06T14:04:16Z","update_time":"2021-10-06T14:19:52Z","links":[{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/33889979KA672323F","rel":"self","method":"GET"}]}',
        ]
        payment = Payment(
            1000,
            'EUR',
            '1234',
            '33889979KA672323F',
        )
        self._service.status(payment)
        # check that the payment object was correctly updated by the mock payment integrations calls
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '33889979KA672323F')

    def test_refund(self):
        self._fake_http_client.data = [
            '{"scope":"https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks","access_token":"A21AAKRdHNBqKUbNWaLt11sn0Too21Y42GpMif5_dMjvXAdjlLjuPv1mvKpSdaGvCs2rofTsAMKo_VFpyYMh1YNINHmGyG0sg","token_type":"Bearer","app_id":"APP-80W284485P519543T","expires_in":32384,"nonce":"2021-10-06T14:02:50Z52w3KxZIG9RFpjQaWMvj4oiL6mGaxR4-YEqzpNVQ6jE"}',
            '{"id":"33889979KA672323F","intent":"CAPTURE","status":"COMPLETED","purchase_units":[{"reference_id":"TST2621100616040887","amount":{"currency_code":"EUR","value":"1.00"},"payee":{"email_address":"dev-facilitator@iraiser.eu","merchant_id":"6LCX48AYE8CJW"},"description":"1006/TST2621100616040887/2/","payments":{"captures":[{"id":"2DW1411898692761B","status":"COMPLETED","amount":{"currency_code":"EUR","value":"1.00"},"final_capture":true,"seller_protection":{"status":"ELIGIBLE","dispute_categories":["ITEM_NOT_RECEIVED","UNAUTHORIZED_TRANSACTION"]},"seller_receivable_breakdown":{"gross_amount":{"currency_code":"EUR","value":"1.00"},"paypal_fee":{"currency_code":"EUR","value":"0.44"},"net_amount":{"currency_code":"EUR","value":"0.56"}},"links":[{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2DW1411898692761B","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2DW1411898692761B/refund","rel":"refund","method":"POST"},{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/33889979KA672323F","rel":"up","method":"GET"}],"create_time":"2021-10-06T14:19:52Z","update_time":"2021-10-06T14:19:52Z"}]}}],"payer":{"name":{"given_name":"yann","surname":"jacob"},"email_address":"yjacob+paypal@iraiser.eu","payer_id":"H2HNX5QTLYJZC","address":{"address_line_1":"199 route de clisson","admin_area_2":"saint sebastien sur loire","postal_code":"44230","country_code":"FR"}},"create_time":"2021-10-06T14:04:16Z","update_time":"2021-10-06T14:19:52Z","links":[{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/33889979KA672323F","rel":"self","method":"GET"}]}',
            '{"id":"52V51802J2543164M","amount":{"currency_code":"EUR","value":"1.00"},"seller_payable_breakdown":{"gross_amount":{"currency_code":"EUR","value":"1.00"},"paypal_fee":{"currency_code":"EUR","value":"0.05"},"net_amount":{"currency_code":"EUR","value":"0.95"},"total_refunded_amount":{"currency_code":"EUR","value":"1.00"}},"invoice_id":"TST2621100616040887","status":"COMPLETED","create_time":"2021-10-06T07:31:16-07:00","update_time":"2021-10-06T07:31:16-07:00","links":[{"href":"https://api.sandbox.paypal.com/v2/payments/refunds/52V51802J2543164M","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v2/payments/captures/2DW1411898692761B","rel":"up","method":"GET"}]}',
        ]
        payment = Payment(
            1000,
            'EUR',
            '1234',
            '33889979KA672323F',
        )
        self._service.refund(payment)
        # check that the payment object was correctly updated by the mock payment integrations calls
        self.assertEqual(payment.status, PaymentStatus.REFUNDED)
        self.assertEqual(payment.gateway_status, 'COMPLETED')
        self.assertEqual(payment.gateway_id, '52V51802J2543164M')
