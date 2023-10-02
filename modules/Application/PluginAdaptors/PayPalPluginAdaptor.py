from abc import ABC

from modules.Domain.Plugins.AbstractPayPalPlugin import PayPalPlugin
from modules.Entities import Payment
from modules.Entities.Payer import Payer
from .CreateOrder.CreateOrderRequest import CreateOrderRequest
from .CreateOrder.CreateOrderResponse import CreateOrderResponse
from .GetAccessToken.GetAccessTokenRequest import GetAccessTokenRequest
from .GetAccessToken.GetAccessTokenResponse import GetAccessTokenResponse
from .CapturePaymentForOrder.CapturePaymentForOrderRequest import CapturePaymentForOrderRequest
from .CapturePaymentForOrder.CapturePaymentForOrderResponse import CapturePaymentForOrderResponse
from .ShowOrderDetails.ShowOrderDetailsRequest import ShowOrderDetailsRequest
from .ShowOrderDetails.ShowOrderDetailsResponse import ShowOrderDetailsResponse
from .RefundCapturedPayment.RefundCapturedPaymentRequest import RefundCapturedPaymentRequest
from .RefundCapturedPayment.RefundCapturedPaymentResponse import RefundCapturedPaymentResponse
from .HTTPClientInterface import HTTPClientInterface


class PayPalPluginAdaptor(PayPalPlugin, ABC):
    http_client_interface: HTTPClientInterface

    def __init__(self, client_id: str, client_secret: str, http_client_interface: HTTPClientInterface):
        super().__init__(client_id, client_secret)
        self.http_client_interface = http_client_interface

    def get_access_token(self) -> GetAccessTokenResponse:
        request = GetAccessTokenRequest(self)
        response = GetAccessTokenResponse(request.send())
        self.access_token = response.get_access_token()
        return response

    def create_order(self, payment: Payment, payer: Payer) -> CreateOrderResponse:
        request = CreateOrderRequest(self, payment, payer)
        response = CreateOrderResponse(request.send(), payment)
        response.update_payment()
        return response

    def capture_payment_for_order(self, payment: Payment) -> CapturePaymentForOrderResponse:
        request = CapturePaymentForOrderRequest(self, payment)
        response = CapturePaymentForOrderResponse(request.send(), payment)
        response.update_payment()
        return response

    def refund_captured_payment(self, payment: Payment) -> RefundCapturedPaymentResponse:
        request = RefundCapturedPaymentRequest(self, payment)
        response = RefundCapturedPaymentResponse(request.send(), payment)
        response.update_payment()
        return response

    def show_order_details(self, payment: Payment) -> ShowOrderDetailsResponse:
        request = ShowOrderDetailsRequest(self, payment)
        response = ShowOrderDetailsResponse(request.send(), payment)
        response.update_payment()
        return response
