# -*- coding: utf-8 -*-
import unittest
from modules.entities.product import Product
from modules.entities.cart import Cart
from modules.presentation.cart import display_cart_json, display_cart_xml


class TestCartPresentation(unittest.TestCase):
    def test_json(self):
        cart = Cart()
        cart.add_product(Product('AAA100', 100, 1, 0), 1)
        cart.add_product(Product('BBB100', 200, 2, 0), 2)
        self.assertEqual(display_cart_json(cart, 1), {
            'content': [{'reference': 'AAA100', 'price': 100, 'number': 1},
                         {'reference': 'BBB100', 'price': 200, 'number': 2}],
            'value': 500})
