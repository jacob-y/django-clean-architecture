from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_202_ACCEPTED
from modules.Domain.Services.PayPalService import PayPalService
from modules.Domain.Services.StripeService import StripeService
from modules.Application.PluginAdaptors.PayPal.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Application.PluginAdaptors.Stripe.StripePluginAdaptor import StripePluginAdaptor
from modules.Application.PortAdaptors.PaymentAPIPortAdaptor import PaymentAPIPortAdaptor
from modules.Application.ModelAdaptors.FileStorage import FileStorage


def _initialize_service(payment_gateway: str):
    file_storage = FileStorage()
    match payment_gateway:
        case 'stripe':
            return StripeService(
                StripePluginAdaptor(
                    file_storage.get_stripe_secret_key()
                )
            )
        case 'paypal':
            return PayPalService(
                PayPalPluginAdaptor(
                    file_storage.get_paypal_client_id(),
                    file_storage.get_paypal_client_secret()
                )
            )
        case _:
            raise Exception("Invalid payment gateway")


@api_view(['POST'])
def payment_create(request, payment_gateway: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.create_payment(request.data)
    payer = api_adaptor.create_payer(request.data)
    service = _initialize_service(payment_gateway)
    service.pay(payment, payer)
    return Response(payment.to_string(), status=HTTP_201_CREATED)


@api_view(['GET'])
def payment_status(request, payment_gateway: str, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id)
    service = _initialize_service(payment_gateway)
    service.status(payment)
    return Response(payment.to_string(), status=HTTP_200_OK)


@api_view(['POST'])
def payment_capture(request, payment_gateway: str, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id)
    service = _initialize_service(payment_gateway)
    service.capture(payment)
    return Response(payment.to_string(), status=HTTP_202_ACCEPTED)
