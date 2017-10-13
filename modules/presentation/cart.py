# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from modules.presentation.product import display_product_json


def display_cart_json(cart, parity=1):
    content = []
    for ref in cart.bought_products.keys():
        elem = display_product_json(cart.bought_products[ref], parity)
        elem['number'] = cart.product_number[ref]
        content.append(elem)
    return {'content': content, 'value': cart.total_value(parity)}


def display_cart_xml(cart, parity=1):
    root = ET.Element("cart")
    for ref in cart.bought_products.keys():
        ET.SubElement(root, "product", reference=ref, price=cart.bought_products[ref].value(parity),
                      number=cart.product_number[ref])
    ET.SubElement(root, "value", value=cart.total_value(parity))
    return ET.tostring(root)
