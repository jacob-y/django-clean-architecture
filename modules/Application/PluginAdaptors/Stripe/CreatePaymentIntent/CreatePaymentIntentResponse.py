from modules.Application.PluginAdaptors.Stripe.StripeResponseMixin import StripeResponseMixin
from modules.Entities.Payment import PaymentMethod


class CreatePaymentIntentResponse(StripeResponseMixin):

    def is_successful(self) -> bool:
        return self._data.get('status') == self.PAYMENT_INTENT_SUCCEEDED

    def is_pending(self) -> bool:
        return self._data.get('status') in [
            self.PAYMENT_INTENT_REQUIRES_ACTION,
            self.PAYMENT_INTENT_REQUIRES_PAYMENT_METHOD,
            self.PAYMENT_INTENT_PROCESSING,
            self.PAYMENT_INTENT_REQUIRES_CAPTURE,
            self.PAYMENT_INTENT_REQUIRES_CONFIRMATION,
            self.PAYMENT_INTENT_REQUIRES_SOURCE_ACTION,
            self.PAYMENT_INTENT_REQUIRES_SOURCE
        ]

    def is_failed(self) -> bool:
        return self._data.get('status') == self.PAYMENT_INTENT_CANCELED

    def error_message(self) -> str | None:
        error = self._data.get('last_payment_error', {})
        if error:
            return error.get('message') or super().error_message()
        return super().error_message()

    def error_code(self) -> str | None:
        error = self._data.get('last_payment_error', {})
        if error:
            return self._data.get('last_payment_error', {}).get('code') or super().error_code()
        return super().error_code()

    def payment_id(self) -> str:
        return self._data.get('latest_charge') or self._data.get('id')

    def redirect_url(self) -> str | None:
        next_action = self._data.get('next_action', {})
        if next_action:
            return next_action.get('redirect_to_url', {}).get('url')
        return None

    def payment_method(self) -> PaymentMethod | None:
        method = self._data.get('payment_method_types', [None])[0]
        match method:
            case 'card':
                return PaymentMethod.CARD
            case 'sepa_debit':
                return PaymentMethod.SEPA_DIRECT_DEBIT
            case _:
                return None
