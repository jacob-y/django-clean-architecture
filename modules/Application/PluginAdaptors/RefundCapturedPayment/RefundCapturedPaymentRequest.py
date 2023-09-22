from ..AbstractPayPalRequest import AbstractPayPalRequest


class RefundCapturedPaymentRequest(AbstractPayPalRequest):

    def _data(self) -> dict:
        return {}

    def _endpoint(self) -> str:
        return super()._endpoint() + '/v2/payments/captures/' + self._payment.capture_id + '/refund'

    def _method(self) -> str:
        return 'POST'
