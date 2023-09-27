from ..AbstractPayPalResponse import AbstractPayPalResponse


class RefundCapturedPaymentResponse(AbstractPayPalResponse):

    def is_successful(self):
        return self._data.get('status') == 'CANCELLED'

    def is_refunded(self) -> bool:
        return self._data.get('status') in ['COMPLETED']

    def is_pending(self):
        return self._data.get('status') in ['PENDING']

    def redirect_url(self) -> str | None:
        return None

    def capture_id(self) -> str | None:
        return None
