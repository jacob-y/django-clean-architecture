from modules.Domain.Ports.PaymentAPIPortInterface import PaymentAPIPort
from modules.Entities.Payer import Payer
from modules.Entities.Payment import Payment, PaymentMethod
from modules.Entities.Card import Card
from modules.Entities.Iban import Iban


class PaymentAPIPortAdaptor(PaymentAPIPort):

    def create_payment(self, data: dict) -> Payment:
        for required_field in [
            'amount', 'currency', 'transaction_id', 'return_url', 'payment_method'
        ]:
            if data.get(required_field) is None:
                raise Exception(f'The field {required_field} is required')
            payment = Payment(
                data['amount'],
                data['currency'],
                data['transaction_id'],
                None,
                data['return_url'],
                PaymentMethod[str.upper(data['payment_method'])],
            )

            if payment.payment_method == PaymentMethod.CARD:
                if card_data := data.get('card'):
                    if card_data.get('token') and card_data.get('last_4_numbers') and \
                            card_data.get('expiry_month') and card_data.get('expiry_year') and \
                            card_data.get('brand'):
                        payment.card = Card(
                            card_data.get('token'),
                            card_data.get('last_4_numbers'),
                            card_data.get('expiry_month'),
                            card_data.get('expiry_year'),
                            card_data.get('brand')
                        )
                else:
                    raise Exception('The field card is required for the payment method CARD')

            if payment.payment_method == PaymentMethod.SEPA_DIRECT_DEBIT:
                if iban_data := data.get('iban'):
                    if iban_data.get('iban') and iban_data.get('bic'):
                        payment.iban = Iban(iban=iban_data.get('iban'), bic=iban_data.get('bic'))
                else:
                    raise Exception('The field iban is required for the payment method SEPA_DIRECT_DEBIT')
        return payment

    def create_payer(self, data: dict) -> Payer:
        for required_field in [
            'first_name', 'last_name', 'email', 'address1', 'city', 'country_code', 'post_code', 'lang'
        ]:
            if data.get(required_field) is None:
                raise Exception(f'The field {required_field} is required')
        return Payer(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['address1'],
            data.get('address2'),
            data['city'],
            data['country_code'],
            data['post_code'],
            data['lang']
        )

    def get_payment(self, gateway_id: str) -> Payment:
        return Payment(gateway_id=gateway_id)
