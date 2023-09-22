from modules.Application.PluginAdaptors.Stripe.StripeResponseMixin import StripeResponseMixin
from modules.Entities.Payment import PaymentMethod


class RetrieveChargeResponse(StripeResponseMixin):

    def is_successful(self) -> bool:
        return self._data.get('status') == self.CHARGE_STATUS_SUCCEEDED

    def is_pending(self) -> bool:
        return self._data.get('status') == self.CHARGE_STATUS_PENDING

    def is_failed(self) -> bool:
        return self._data.get('status') == self.CHARGE_STATUS_FAILED

    def payment_id(self) -> str:
        return self._data.get('id')

    def payment_method(self) -> PaymentMethod | None:
        method = self._data.get('payment_method_details', {}).get('type')
        match method:
            case 'card':
                return PaymentMethod.CARD
            case 'sepa_debit':
                return PaymentMethod.SEPA_DIRECT_DEBIT
            case _:
                return None
