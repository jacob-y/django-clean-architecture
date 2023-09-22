from modules.Domain.Plugins.AbstractResponse import AbstractResponse
from abc import ABC


class StripeResponseMixin(AbstractResponse):
    PAYMENT_INTENT_SUCCEEDED = 'succeeded'
    PAYMENT_INTENT_PROCESSING = 'processing'
    PAYMENT_INTENT_CANCELED = 'canceled'
    PAYMENT_INTENT_REQUIRES_CONFIRMATION = 'requires_confirmation'
    PAYMENT_INTENT_REQUIRES_SOURCE_ACTION = 'requires_source_action'
    PAYMENT_INTENT_REQUIRES_ACTION = 'requires_action'
    PAYMENT_INTENT_REQUIRES_CAPTURE = 'requires_capture'
    PAYMENT_INTENT_REQUIRES_PAYMENT_METHOD = 'requires_payment_method'
    PAYMENT_INTENT_REQUIRES_SOURCE = 'requires_source'

    CHARGE_STATUS_SUCCEEDED = 'succeeded'
    CHARGE_STATUS_PENDING = 'pending'
    CHARGE_STATUS_FAILED = 'failed'

    REFUND_STATUS_SUCCEEDED = 'succeeded'
    REFUND_STATUS_PENDING = 'pending'
    REFUND_STATUS_FAILED = 'failed'

    def error_message(self) -> str | None:
        return self._data.get('details') and self._data.get('details')[0].get('description') \
            or self._data.get('error', {}).get('message') \
            or self._data.get('message')

    def error_code(self) -> str | None:
        return self._data.get('details') and self._data.get('details')[0].get('issue') \
            or self._data.get('details') \
            or self._data.get('error', {}).get('name') \
            or self._data.get('name')

    def payment_id(self) -> str:
        return self._data.get('id')

    def gateway_status(self) -> str | None:
        return self._data.get('status')
