from modules.Application.PluginAdaptors.PayPal.PayPalHTTPMixin import PayPalHTTPMixin
from modules.Entities.Payment import Payment


class CapturePaymentForOrderRequest(PayPalHTTPMixin):
    _payment: Payment

    def __init__(self, payment: Payment, access_token: str):
        self._payment = payment
        self._access_token = access_token

    def _data(self) -> dict:
        return {}

    def _endpoint(self) -> str:
        return super()._url() + '/v2/checkout/orders/' + self._payment.gateway_id + '/capture'

    def _method(self) -> str:
        return 'POST'
