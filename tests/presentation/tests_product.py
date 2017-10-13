# -*- coding: utf-8 -*-
import unittest
from modules.entities.product import Product
from modules.presentation.product import display_product_json, display_product_xml


class TestCartPresentation(unittest.TestCase):
    def test_json(self):
        p = Product('AAA100', 100, 10, 10)
        self.assertEqual(display_product_json(p), {'reference': 'AAA100', 'price': 100})
