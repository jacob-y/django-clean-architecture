import unittest
from time import time
from modules.Entities.Card import Card
from modules.Entities.Iban import Iban
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer
from modules.Domain.Services.StripeService import StripeService
from modules.Application.PluginAdaptors.Stripe.StripePluginAdaptor import StripePluginAdaptor
from modules.Application.ModelAdaptors.FileStorage import FileStorage


class StripeIntegrationTest(unittest.TestCase):

    def test_card(self):
        payment = Payment(int(1000), 'EUR', str(int(time())), None, 'https://127.0.0.1/thank_you',
                          PaymentMethod.CARD,
                          Card('4242424242424242', '12', '26', '123', 'Visa'))
        payer = Payer('John', 'Doe', 'john.doe@example.com',
                      '1 rue des Roses', '2nd Etage', 'Nantes',
                      'FR', '44000', 'fr-FR')
        credentials = FileStorage()
        stripe_plugin = StripePluginAdaptor(
            credentials.get_stripe_secret_key())
        stripe_service = StripeService(stripe_plugin)
        stripe_service.pay(payment, payer)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)
        stripe_service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.SUCCESSFUL)

    def test_iban(self):
        payment = Payment(int(1000), 'EUR', str(int(time())), None, 'https://127.0.0.1/thank_you',
                          PaymentMethod.SEPA_DIRECT_DEBIT,
                          iban=Iban('FR1420041010050500013M02606', 'PSSTFRPPLIL'))
        payer = Payer('John', 'Doe', 'john.doe@example.com',
                      '1 rue des Roses', '2nd Etage', 'Nantes',
                      'FR', '44000', 'fr-FR')
        credentials = FileStorage()
        stripe_plugin = StripePluginAdaptor(
            credentials.get_stripe_secret_key())
        stripe_service = StripeService(stripe_plugin)
        stripe_service.pay(payment, payer)
        # IBAN payments do not self validate immediately
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        stripe_service.status(payment)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
