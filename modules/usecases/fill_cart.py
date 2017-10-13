# -*- coding: utf-8 -*-


def fill_cart(cart, product, number):
    product.add_available(-number)
    product.add_reserved(number)
    cart.add_product(product, number)
    return cart, product
