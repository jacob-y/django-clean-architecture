from modules.Domain.Ports.PaymentAPIPortInterface import PaymentAPIPort
from modules.Entities.Payer import Payer
from modules.Entities.Payment import Payment, PaymentMethod


class PaymentAPIPortAdaptor(PaymentAPIPort):

    def create_payment(self, data: dict, payment_method: str) -> Payment:
        for required_field in [
            'amount', 'currency', 'transaction_id', 'return_url'
        ]:
            if data.get(required_field) is None:
                raise Exception(f'The field {required_field} is required')
        return Payment(data['amount'], data['currency'], data['transaction_id'], None, data['return_url'],
                       PaymentMethod[str.upper(payment_method)], data.get('card'), data.get('iban'))

    def create_payer(self, data: dict) -> Payer:
        for required_field in [
            'first_name', 'last_name', 'email', 'address1', 'city', 'country_code', 'post_code', 'lang'
        ]:
            if data.get(required_field) is None:
                raise Exception(f'The field {required_field} is required')
        return Payer(data['first_name'], data['last_name'], data['email'], data['address1'], data.get('address2'),
                     data['city'], data['country_code'], data['post_code'], data['lang'])

    def get_payment(self, gateway_id: str, payment_method: str) -> Payment:
        return Payment(gateway_id=gateway_id, payment_method=PaymentMethod[str.upper(payment_method)])
