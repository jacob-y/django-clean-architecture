import time
from modules.Entities.Payment import PaymentStatus, PaymentMethod
from modules.Entities.Card import Card
from modules.Entities.Iban import Iban
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_202_ACCEPTED
from modules.Domain.Services.PayPalService import PayPalService
from modules.Domain.Services.StripeService import StripeService
from modules.Application.PluginAdaptors.PayPal.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Application.PluginAdaptors.Stripe.StripePluginAdaptor import StripePluginAdaptor
from modules.Application.PortAdaptors.PaymentAPIPortAdaptor import PaymentAPIPortAdaptor
from modules.Application.ModelAdaptors.FileStorage import FileStorage
from forms.PayPalForm import PayPalForm
from forms.CardForm import CardForm
from forms.IbanForm import IbanForm


def _initialize_paypal_service():
    file_storage = FileStorage()
    paypal_adaptor = PayPalPluginAdaptor(
        file_storage.get_paypal_client_id(), file_storage.get_paypal_client_secret())
    service = PayPalService(paypal_adaptor)
    return service


def _initialize_stripe_service():
    file_storage = FileStorage()
    stripe_adaptor = StripePluginAdaptor(
        file_storage.get_stripe_secret_key())
    service = StripeService(stripe_adaptor)
    return service


def _initialize_service(payment_method: PaymentMethod):
    match payment_method:
        case PaymentMethod.CARD:
            return _initialize_stripe_service()
        case PaymentMethod.SEPA_DIRECT_DEBIT:
            return _initialize_stripe_service()
        case PaymentMethod.PAYPAL:
            return _initialize_paypal_service()
        case _:
            raise Exception("Invalid payment method")


@api_view(['POST'])
def payment_create(request, payment_method: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.create_payment(request.data, payment_method)
    payer = api_adaptor.create_payer(request.data)
    service = _initialize_service(payment.payment_method)
    service.pay(payment, payer)
    return Response(payment.to_string(), status=HTTP_201_CREATED)


@api_view(['GET'])
def payment_status(request, payment_method: str, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id, payment_method)
    service = _initialize_service(payment.payment_method)
    service.status(payment)
    return Response(payment.to_string(), status=HTTP_200_OK)


@api_view(['POST'])
def payment_capture(request, payment_method: str, payment_id: str) -> Response:
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(payment_id, payment_method)
    service = _initialize_service(payment.payment_method)
    service.capture(payment)
    return Response(payment.to_string(), status=HTTP_202_ACCEPTED)


def _payment_form(request, form):
    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/submit/")
    else:
        form = form()
    return render(request, "index.html", {"form": form})


def paypal(request):
    return _payment_form(request, PayPalForm)


def card(request):
    return _payment_form(request, CardForm)


def iban(request):
    return _payment_form(request, IbanForm)


@csrf_protect
def submit(request):
    if not request.method == 'POST':
        raise Exception("Invalid request method")
    payment_method = PaymentMethod(request.POST.get('payment_method'))
    match payment_method:
        case PaymentMethod.CARD:
            form = CardForm(request.POST)
        case PaymentMethod.SEPA_DIRECT_DEBIT:
            form = IbanForm(request.POST)
        case PaymentMethod.PAYPAL:
            form = PayPalForm(request.POST)
        case _:
            raise Exception("Invalid payment method")
    service = _initialize_service(payment_method)
    if not form.is_valid():
        return render(request, "index.html", {"form": form})
    data = {
            "email": form.data['email'],
            "first_name": form.data['first_name'],
            "last_name": form.data['last_name'],
            "address1": form.data['address1'],
            "address2": form.data['address2'],
            "post_code": form.data['postcode'],
            "city": form.data['city'],
            "country_code": form.data['country_code'],
            "transaction_id": "test_form_" + str(time.time()),
            "lang": "fr-FR",
            "amount": form.data['amount'],
            "currency": "EUR",
            "return_url": "http://127.0.0.1:8000/thank_you",
            "payment_method": payment_method,
        }
    match payment_method:
        case PaymentMethod.CARD:
            data['card'] = Card(form.data['number'], form.data['expiry_month'], form.data['expiry_year'],
                                form.data['cvv'], form.data['brand'])
        case PaymentMethod.SEPA_DIRECT_DEBIT:
            data["iban"] = Iban(form.data['iban'], form.data['bic'])
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.create_payment(data, payment_method)
    payer = api_adaptor.create_payer(data)
    service.pay(payment, payer)
    match payment.status:
        case PaymentStatus.PENDING:
            if payment.redirect_url:
                return HttpResponseRedirect(payment.redirect_url)
        case PaymentStatus.SUCCESSFUL:
            return render(request, "thank_you.html", {'payment': payment.to_string()})
    return render(request, "index.html", {"form": form})


def thank_you(request):
    api_adaptor = PaymentAPIPortAdaptor()
    payment = api_adaptor.get_payment(request.GET.get('token'), request.GET.get('payment_method'))
    service = _initialize_service(payment.payment_method)
    service.capture(payment)
    return render(
        request,
        "thank_you.html",
        {'payment': payment.to_string(), 'gateway_id': payment.gateway_id}
    )
