# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


def display_product_json(product, parity=1):
    return {'reference': product.reference, 'price': product.value(parity)}


def display_product_xml(product, parity=1):
    return ET.tostring(ET.Element("product", reference=product.reference,
                                  price=str(product.value(parity))))
