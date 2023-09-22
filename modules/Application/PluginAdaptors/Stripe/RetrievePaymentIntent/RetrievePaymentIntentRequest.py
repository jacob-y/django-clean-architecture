from modules.Entities.Payment import Payment
from stripe import PaymentIntent


class RetrievePaymentIntentRequest:
    _payment: Payment

    def __init__(self, payment: Payment):
        self._payment = payment

    def send(self):
        return PaymentIntent.retrieve(self._payment.gateway_id).to_dict()
