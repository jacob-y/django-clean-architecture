from datetime import datetime
from modules.Entities.Payment import PaymentMethod, Payment
from modules.Entities.Payer import Payer
from stripe import PaymentIntent


class CreatePaymentIntentRequest:
    _payment: Payment
    _payer: Payer

    def __init__(self, payment: Payment, payer: Payer):
        self._payment = payment
        self._payer = payer

    def _data(self) -> dict:

        data = {
            #'description':  f"{str(datetime.month)}{str(datetime.year)}/{self._payment.transaction_id}/",
            'amount': int(self._payment.money.amount * 100), # only works for EUR
            'currency': self._payment.money.currency,
            'payment_method': self._payment.gateway_id,
            'payment_method_options': {},
            'metadata': {
                'number': self._payment.transaction_id,
                'email': self._payer.email,
                'firstname': self._payer.first_name,
                'lastname': self._payer.last_name
            },
            'confirm': True,
            'return_url': self._payment.return_url
        }
        match self._payment.payment_method:
            case PaymentMethod.CARD:
                data['payment_method_types'] = ['card']
                data['payment_method_options']['card'] = {
                    'request_three_d_secure': 'automatic'
                }
                data['statement_descriptor_suffix'] = 'CARD PAYMENT'
            case PaymentMethod.SEPA_DIRECT_DEBIT:
                data['payment_method_types'] = ['sepa_debit']
                data['statement_descriptor'] = 'SEPA PAYMENT'
                data['mandate_data'] = {
                    'customer_acceptance': {
                        'type': 'online',
                        'online': {
                            'ip_address': '127.0.0.1',
                            'user_agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)'
                        }
                    }
                }
        return data

    def send(self):
        return PaymentIntent.create(**self._data()).to_dict()
