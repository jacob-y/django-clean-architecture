from ..AbstractPayPalRequest import AbstractPayPalRequest


class CreateOrderRequest(AbstractPayPalRequest):

    def _data(self) -> dict:
        return {
            'intent': 'CAPTURE',
            'payer': {
                'name': {
                    'given_name': self._payer.first_name,
                    'surname': self._payer.last_name
                },
                'email_address': self._payer.email,
                'address': {
                    'address_line_1': self._payer.address1,
                    'address_line_2': self._payer.address2,
                    'postal_code': self._payer.post_code,
                    'country_code': self._payer.country_code,
                    'admin_area_2': self._payer.city
                }
            },
            'purchase_units': [{
                'amount': {
                    'value': float(self._payment.money.amount),
                    'currency_code': self._payment.money.currency,
                },
                'reference_id': self._payment.transaction_id,
                'description': 'PAYPAL PAYMENT DEMO',
                'invoice_id': self._payment.transaction_id,  # visible to the payer
                'custom_id': 'PAYPAL PAYMENT DEMO'  # not visible to the payer
            }],
            'application_context': {
                'return_url': self._payment.return_url,
                'cancel_url': self._payment.return_url,
                'user_action': 'PAY_NOW',
                'shipping_preference': 'NO_SHIPPING',
                'locale': self._payer.lang
            }
        }

    def _endpoint(self) -> str:
        return super()._endpoint() + '/v2/checkout/orders'

    def _method(self) -> str:
        return 'POST'
