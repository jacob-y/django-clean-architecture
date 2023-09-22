import unittest
from modules.Entities.Payment import Payment


class PaymentTest(unittest.TestCase):

    def test_amount_too_high(self):
        payment = Payment(1000000, 'EUR', '1234')
        with self.assertRaises(Exception) as e:
            payment.check()
            self.assertEquals('The amount must be between 1 and 10 000 of the currency unit', e.exception.args[0])
