from ..AbstractPayPalRequest import AbstractPayPalRequest


class ShowOrderDetailsRequest(AbstractPayPalRequest):

    def _data(self) -> dict:
        return {}

    def _endpoint(self) -> str:
        return super()._endpoint() + '/v2/checkout/orders/' + self._payment.gateway_id

    def _method(self) -> str:
        return 'GET'
