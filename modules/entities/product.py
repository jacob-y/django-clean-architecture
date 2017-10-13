# -*- coding: utf-8 -*-
import re


class NullOrNegativePriceException(Exception):
    pass


class NullOrNegativeParityException(Exception):
    pass


class InvalidReference(Exception):
    pass


class TooManyProductsRemoved(Exception):
    pass


class Product:
    """
    here is the buisness logic of product entity
    """
    def __init__(self, reference, price, nb_reserved, nb_available):
        if price <= 0:
            raise NullOrNegativePriceException
        pattern = re.compile("^[A-Z]+[0-9]+$")
        if not pattern.match(reference):
            raise InvalidReference
        self.reference = reference
        self.price = price
        self.nb_reserved = nb_reserved
        self.nb_available = nb_available

    def value(self, parity):
        return self.price * parity

    def add_reserved(self, number):
        self.nb_reserved += number

    def add_available(self, number):
        if self.nb_available + number < 0:
            raise TooManyProductsRemoved()
        self.nb_available += number
