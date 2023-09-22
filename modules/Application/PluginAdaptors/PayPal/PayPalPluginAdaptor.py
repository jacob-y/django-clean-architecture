from abc import ABC

from modules.Domain.Plugins.AbstractPayPalPlugin import PayPalPlugin
from modules.Entities import Payment
from modules.Entities.Payer import Payer
from modules.Application.PluginAdaptors.PayPal.CreateOrder.CreateOrderRequest import CreateOrderRequest
from modules.Application.PluginAdaptors.PayPal.CreateOrder.CreateOrderResponse import CreateOrderResponse
from modules.Application.PluginAdaptors.PayPal.GetAccessToken.GetAccessTokenRequest import GetAccessTokenRequest
from modules.Application.PluginAdaptors.PayPal.GetAccessToken.GetAccessTokenResponse import GetAccessTokenResponse
from modules.Application.PluginAdaptors.PayPal.CapturePaymentForOrder.CapturePaymentForOrderRequest import CapturePaymentForOrderRequest
from modules.Application.PluginAdaptors.PayPal.CapturePaymentForOrder.CapturePaymentForOrderResponse import CapturePaymentForOrderResponse
from modules.Application.PluginAdaptors.PayPal.ShowOrderDetails.ShowOrderDetailsRequest import ShowOrderDetailsRequest
from modules.Application.PluginAdaptors.PayPal.ShowOrderDetails.ShowOrderDetailsResponse import ShowOrderDetailsResponse


class PayPalPluginAdaptor(PayPalPlugin, ABC):
    access_token: str | None = None

    def get_access_token(self) -> GetAccessTokenResponse:
        request = GetAccessTokenRequest(self.client_id, self.client_secret)
        response = GetAccessTokenResponse(request.send())
        self.access_token = response.get_access_token()
        return response

    def create_order(self, payment: Payment, payer: Payer) -> CreateOrderResponse:
        request = CreateOrderRequest(payment, payer, self.access_token)
        return CreateOrderResponse(request.send(), payment)

    def capture_payment_for_order(self, payment: Payment) -> CapturePaymentForOrderResponse:
        request = CapturePaymentForOrderRequest(payment, self.access_token)
        return CapturePaymentForOrderResponse(request.send(), payment)

    def show_order_details(self, payment: Payment) -> ShowOrderDetailsResponse:
        request = ShowOrderDetailsRequest(payment, self.access_token)
        return ShowOrderDetailsResponse(request.send(), payment)
