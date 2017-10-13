# -*- coding: utf-8 -*-
from modules.entities.product import NullOrNegativeParityException


class NullOrNegativeProductAddedException(Exception):
    pass


class Cart:
    def __init__(self):
        self.product_number = {}
        self.bought_products = {}

    def add_product(self, product, number):
        if number <= 0:
            raise NullOrNegativeProductAddedException()
        if product.reference not in self.product_number.keys():
            self.product_number[product.reference] = 0
            self.bought_products[product.reference] = product
        self.product_number[product.reference] += number

    def total_value(self, parity):
        if parity <= 0:
            raise NullOrNegativeParityException()
        return sum([self.bought_products[ref].price * self.product_number[ref] * parity
                    for ref in self.bought_products.keys()])
