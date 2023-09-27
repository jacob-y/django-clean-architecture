from ..AbstractPayPalResponse import AbstractPayPalResponse


class CapturePaymentForOrderResponse(AbstractPayPalResponse):

    def is_successful(self):
        return self._data.get('status') == 'COMPLETED'

    def is_refunded(self) -> bool:
        return False

    def is_pending(self):
        return self._data.get('status') in ['CREATED', 'SAVED', 'APPROVED', 'PAYER_ACTION_REQUIRED']

    def redirect_url(self) -> str | None:
        return None
