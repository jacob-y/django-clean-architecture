from modules.Entities.Payer import Payer
from modules.Entities.Payment import Payment, PaymentMethod
from stripe import PaymentMethod


class CreatePaymentMethodRequest:
    _payment: Payment
    _payer: Payer

    def __init__(self, payment: Payment, payer: Payer):
        self._payment = payment
        self._payer = payer

    def _data(self) -> dict:
        # stripe reject the payment is there is empty address fields
        # because they are seen as a bad field "update"
        address = {}
        if self._payer.address1:
            address['line1'] = self._payer.address1
        if self._payer.address2:
            address['line2'] = self._payer.address2
        if self._payer.post_code:
            address['postal_code'] = self._payer.post_code
        if self._payer.city:
            address['city'] = self._payer.city
        if self._payer.country_code:
            address['country'] = self._payer.country_code

        data = {
            'billing_details': {
                'name': self._payer.full_name(),
                'email': self._payer.email,
                'address': address
            }
        }

        match self._payment.payment_method:
            case 'sepa':
                data['type'] = 'sepa_debit'
                data['sepa_debit'] = {
                    'iban': self._payment.iban.iban
                }
        return data

    def send(self) -> dict:
        return PaymentMethod.create(**self._data()).to_dict()
