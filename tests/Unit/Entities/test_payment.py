import unittest
from modules.Entities.Payment import Payment
from modules.Entities.Card import Card


class PaymentTest(unittest.TestCase):

    def test_amount_too_high(self):
        payment = Payment(1000000, 'EUR', '1234')
        with self.assertRaises(Exception) as e:
            payment.check()
            self.assertEquals('The amount must be between 1 and 10 000 of the currency unit', e.exception.args[0])

    def test_card_invalid_numbers(self):
        card = Card('1234ABCD', '123', '12', '25', 'Visa')
        payment = Payment(100, 'EUR', '1234', card=card)
        with self.assertRaises(Exception) as e:
            payment.check()
            self.assertEquals('The card data is invalid', e.exception.args[0])
