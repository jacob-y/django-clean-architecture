from modules.Domain.Plugins.AbstractResponse import AbstractResponse
from modules.Entities.Payment import PaymentMethod


class PayPalResponseMixin(AbstractResponse):

    ORDER_CREATED = 'CREATED'
    ORDER_SAVED = 'SAVED'
    ORDER_APPROVED = 'APPROVED'
    ORDER_VOIDED = 'VOIDED'
    ORDER_PARTIALLY_COMPLETED = 'PARTIALLY_COMPLETED'
    ORDER_COMPLETED = 'COMPLETED'
    ORDER_PAYER_ACTION_REQUIRED = 'PAYER_ACTION_REQUIRED'

    CAPTURE_COMPLETED = 'COMPLETED'
    CAPTURE_DECLINED = 'DECLINED'
    CAPTURE_PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED'
    CAPTURE_PENDING = 'PENDING'
    CAPTURE_REFUNDED = 'REFUNDED'
    CAPTURE_FAILED = 'FAILED'

    REFUND_CANCELLED = 'CANCELLED'
    REFUND_PENDING = 'PENDING'
    REFUND_COMPLETED = 'COMPLETED'

    def error_message(self) -> str | None:
        details = self._data.get('details')
        if details and details[0].get('description'):
            return details[0].get('description')
        return self._data.get('error_description') or self._data.get('message')

    def error_code(self) -> str | None:
        details = self._data.get('details')
        if details and details[0].get('issue'):
            return details[0].get('issue')
        return self._data.get('error') or self._data.get('name')

    def payment_id(self) -> str:
        return self._data.get('id')

    def capture_id(self) -> str | None:
        return None

    def gateway_status(self) -> str | None:
        return self._data.get('status') or None

    def payment_method(self) -> PaymentMethod | None:
        return PaymentMethod.PAYPAL
