from modules.Application.PluginAdaptors.Stripe.StripeResponseMixin import StripeResponseMixin
from modules.Entities.Payment import PaymentMethod


class RetrievePaymentMethodResponse(StripeResponseMixin):
    def is_pending(self) -> bool:
        return bool(self._data.get('id'))

    def gateway_id(self):
        return self._data.get('id')

    def payment_method(self) -> PaymentMethod | None:
        method = self._data.get('type')
        match method:
            case 'card':
                return PaymentMethod.CARD
            case 'sepa_debit':
                return PaymentMethod.SEPA_DIRECT_DEBIT
            case _:
                return None
