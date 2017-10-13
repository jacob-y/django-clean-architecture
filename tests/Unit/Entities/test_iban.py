from unittest import TestCase
from modules.Entities.Iban import Iban


class IbanTest(TestCase):

    def test_mask(self):
        iban = Iban('DE89370400440532013000', 'COBADEFFXXX')
        self.assertEqual('**************32013000', iban.mask())
