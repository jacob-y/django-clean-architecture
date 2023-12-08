import unittest
from time import time
from modules.Entities.Payment import Payment, PaymentStatus
from modules.Entities.Payer import Payer
from modules.Domain.Services.PayPalService import PayPalService
from modules.Application.PluginAdaptors.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Infrastructure.RequestsClient import RequestsClient
from modules.Application.ModelAdaptors.FileStorage import FileStorage


class PaymentTest(unittest.TestCase):

    def test_start_payment(self):
        payment = Payment(int(1000), 'EUR', str(int(time())), None, 'https://iraiser.eu')
        payer = Payer('yann', 'jacob', 'yjacob+paypal@iraiser.eu', '199 route de clisson', '2nd Etage', 'Saint Sébastien Sur Loire', 'FR', '44230', 'fr-FR')
        http_client = RequestsClient()
        credentials = FileStorage()
        paypal_plugin = PayPalPluginAdaptor(credentials.get_paypal_client_id(), credentials.get_paypal_client_secret(), http_client)
        paypal_service = PayPalService(paypal_plugin)
        paypal_service.pay(payment, payer)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        paypal_service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
