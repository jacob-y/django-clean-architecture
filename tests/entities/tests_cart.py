# -*- coding: utf-8 -*-
import unittest
from modules.entities.cart import Cart, NullOrNegativeParityException
from modules.entities.product import Product


class TestCart(unittest.TestCase):

    def test(self):
        cart = Cart()
        cart.add_product(Product('REF1', 100, 0 ,0), 1)
        cart.add_product(Product('REF2', 1000,0 ,0), 2)
        self.assertEqual(cart.total_value(1), 2100)
        self.assertEqual(cart.total_value(2), 4200)
        with self.assertRaises(NullOrNegativeParityException):
            cart.total_value(0)
