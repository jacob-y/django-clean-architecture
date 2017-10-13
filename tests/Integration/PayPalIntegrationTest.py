import unittest
from time import time
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer
from modules.Domain.Services.PayPalService import PayPalService
from modules.Application.PluginAdaptors.PayPal.PayPalPluginAdaptor import PayPalPluginAdaptor
from modules.Application.ModelAdaptors.FileStorage import FileStorage


class PayPalIntegrationTest(unittest.TestCase):

    def test_paypal(self):
        payment = Payment(int(1000), 'EUR', str(int(time())), None,
                          'https://127.0.0.1/thank_you', PaymentMethod.PAYPAL)
        payer = Payer('John', 'Doe', 'john.doe@example.com',
                      '1 rue des Roses', '2nd Etage', 'Nantes',
                      'FR', '44000', 'fr-FR')
        credentials = FileStorage()
        paypal_plugin = PayPalPluginAdaptor(
            credentials.get_paypal_client_id(), credentials.get_paypal_client_secret())
        paypal_service = PayPalService(paypal_plugin)
        paypal_service.pay(payment, payer)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        paypal_service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        # the rest of the workflow requires to connect on the web UI, can not test further
