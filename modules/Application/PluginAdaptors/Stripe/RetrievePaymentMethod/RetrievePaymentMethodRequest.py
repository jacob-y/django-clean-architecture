from modules.Entities.Payment import Payment
from stripe import PaymentMethod


class RetrievePaymentMethodRequest:
    _payment: Payment

    def __init__(self, payment: Payment):
        self._payment = payment

    def send(self):
        return PaymentMethod.retrieve(self._payment.gateway_id).to_dict()
