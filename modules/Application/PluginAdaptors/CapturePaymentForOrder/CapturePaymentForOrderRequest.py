from ..AbstractPayPalRequest import AbstractPayPalRequest


class CapturePaymentForOrderRequest(AbstractPayPalRequest):

    def _data(self) -> dict:
        return {}

    def _endpoint(self) -> str:
        return super()._endpoint() + '/v2/checkout/orders/' + self._payment.gateway_id + '/capture'

    def _method(self) -> str:
        return 'POST'
