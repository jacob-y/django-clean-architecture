
from django.test import TestCase
from modules.entities.product import Product
from modules.entities.cart import Cart
from postgres_api.queries import ProductRecords, CartRecords


class TestQueries(TestCase):
    def test_product_records(self):
        ProductRecords.create('AAA100', 1000)
        ProductRecords.create('BBB100', 2000)
        self.assertEqual(ProductRecords.get_by_reference('CCC100'), None)
        self.assertEqual(ProductRecords.get_by_reference('AAA100').__dict__,
                         Product('AAA100', 1000).__dict__)

    def test_cart_records(self):
        CartRecords.create('test1')
        self.assertEqual(CartRecords.get_by_identifier('test1').__dict__, Cart().__dict__)
