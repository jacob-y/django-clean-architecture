# -*- coding: utf-8 -*-
import unittest
from modules.entities.product import Product, NullOrNegativePriceException, InvalidReference


class TestProduct(unittest.TestCase):

    def test(self):
        with self.assertRaises(NullOrNegativePriceException):
            Product('REF1', 0, 0, 0)
        with self.assertRaises(InvalidReference):
            Product('ReF1', 1000, 0, 0)
        Product('REF1', 1000, 0, 0)
