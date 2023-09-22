from abc import ABC

from modules.Domain.Plugins.AbstractStripePlugin import StripePlugin
from modules.Entities import Payment
from modules.Entities.Payer import Payer
from modules.Application.PluginAdaptors.Stripe.CreatePaymentMethod.CreatePaymentMethodRequest import CreatePaymentMethodRequest
from modules.Application.PluginAdaptors.Stripe.CreatePaymentIntent.CreatePaymentIntentResponse import CreatePaymentIntentResponse
from modules.Application.PluginAdaptors.Stripe.CreatePaymentIntent.CreatePaymentIntentRequest import CreatePaymentIntentRequest
from modules.Application.PluginAdaptors.Stripe.CreatePaymentMethod.CreatePaymentMethodResponse import CreatePaymentMethodResponse
from modules.Application.PluginAdaptors.Stripe.RetrievePaymentIntent.RetrievePaymentIntentRequest import RetrievePaymentIntentRequest
from modules.Application.PluginAdaptors.Stripe.RetrievePaymentIntent.RetrievePaymentIntentResponse import RetrievePaymentIntentResponse
from modules.Application.PluginAdaptors.Stripe.RetrieveCharge.RetrieveChargeRequest import RetrieveChargeRequest
from modules.Application.PluginAdaptors.Stripe.RetrieveCharge.RetrieveChargeResponse import RetrieveChargeResponse
from modules.Application.PluginAdaptors.Stripe.RetrievePaymentMethod.RetrievePaymentMethodRequest import RetrievePaymentMethodRequest
from modules.Application.PluginAdaptors.Stripe.RetrievePaymentMethod.RetrievePaymentMethodResponse import RetrievePaymentMethodResponse
import stripe


class StripePluginAdaptor(StripePlugin, ABC):

    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        stripe.api_key = secret_key

    def create_payment_intent(self, payment: Payment, payer: Payer) -> CreatePaymentIntentResponse:
        request = CreatePaymentIntentRequest(payment, payer)
        return CreatePaymentIntentResponse(request.send(), payment)

    def create_payment_method(self, payment: Payment, payer: Payer) -> CreatePaymentMethodResponse:
        request = CreatePaymentMethodRequest(payment, payer)
        return CreatePaymentMethodResponse(request.send(), payment)

    def retrieve_payment_intent(self, payment: Payment) -> RetrievePaymentIntentResponse:
        request = RetrievePaymentIntentRequest(payment)
        return RetrievePaymentIntentResponse(request.send(), payment)

    def retrieve_charge(self, payment: Payment) -> RetrieveChargeResponse:
        request = RetrieveChargeRequest(payment)
        return RetrieveChargeResponse(request.send(), payment)

    def retrieve_payment_method(self, payment: Payment) -> RetrievePaymentMethodResponse:
        request = RetrievePaymentMethodRequest(payment)
        return RetrievePaymentMethodResponse(request.send(), payment)
