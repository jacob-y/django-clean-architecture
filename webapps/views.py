from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_202_ACCEPTED
from modules.Domain.Services.PayPalService import PayPalService
from modules.Application.PluginAdaptors.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Application.PortAdaptors.PaymentAPIPortAdaptor import PaymentAPIPortAdaptor
from modules.Application.ModelAdaptors.FileStorage import FileStorage
from modules.Infrastructure.RequestsClient import RequestsClient


@api_view(['POST'])
def payment_create(request) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.create_payment(request.data)
    payer = api_adaptor.create_payer(request.data)
    file_storage = FileStorage()
    http_client = RequestsClient()
    paypal_adaptor = PayPalPluginAdaptor(
        file_storage.get_paypal_client_id(), file_storage.get_paypal_client_secret(), http_client)
    service = PayPalService(paypal_adaptor)
    service.pay(payment, payer)
    return Response(payment.to_string(), status=HTTP_201_CREATED)


@api_view(['GET'])
def payment_status(request, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id)
    file_storage = FileStorage()
    http_client = RequestsClient()
    paypal_adaptor = PayPalPluginAdaptor(
        file_storage.get_paypal_client_id(), file_storage.get_paypal_client_secret(), http_client)
    service = PayPalService(paypal_adaptor)
    service.status(payment)
    return Response(payment.to_string(), status=HTTP_200_OK)


@api_view(['POST'])
def payment_capture(request, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id)
    file_storage = FileStorage()
    http_client = RequestsClient()
    paypal_adaptor = PayPalPluginAdaptor(
        file_storage.get_paypal_client_id(), file_storage.get_paypal_client_secret(), http_client)
    service = PayPalService(paypal_adaptor)
    service.capture(payment)
    return Response(payment.to_string(), status=HTTP_202_ACCEPTED)


@api_view(['POST'])
def payment_refund(request, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id)
    file_storage = FileStorage()
    http_client = RequestsClient()
    paypal_adaptor = PayPalPluginAdaptor(
        file_storage.get_paypal_client_id(), file_storage.get_paypal_client_secret(), http_client)
    service = PayPalService(paypal_adaptor)
    service.refund(payment)
    return Response(payment.to_string(), status=HTTP_202_ACCEPTED)
