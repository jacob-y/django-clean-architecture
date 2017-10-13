from django.core.exceptions import ObjectDoesNotExist
from postgres_api.models import ProductORM, CartORM, CartProductORM
from modules.entities.product import Product
from modules.entities.cart import Cart


class ProductRecords:

    @staticmethod
    def get_by_reference(reference):
        try:
            product_orm = ProductORM.objects.get(reference=reference)
            return Product(price=product_orm.price, reference=product_orm.reference,
                           nb_reserved=product_orm.nb_reserved,
                           nb_available=product_orm.nb_available)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(reference, price):
        out = Product(reference, price, 0, 0)
        ProductORM.objects.create(reference=reference, price=price)
        return out

    @staticmethod
    def update(reference, product):
        p = ProductORM.objects.get(reference=reference)
        p.nb_reserved = product.nb_reserved
        p.nb_available = product.nb_available
        p.save()


class CartRecords:

    @staticmethod
    def get_by_identifier(identifier):
        try:
            CartORM.objects.get(identifier=identifier)  # raise Exception if no cart
            products = CartProductORM.objects.filter(cart__identifier=identifier).values()
            cart = Cart()
            for product in products:
                cart.add_product(Product(product.reference, product.price,
                                         product.nb_reserved, product.nb_available),
                                 product.number)
            return cart
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(identifier):
        out = Cart()
        CartORM.objects.create(identifier=identifier)
        return out

    @staticmethod
    def update(identifier, cart, reference):
        try:
            elem = CartProductORM.objects.get(product__reference=reference,
                                              cart__identifier=identifier)
            elem.number = cart.product_number[reference]
            elem.save()
        except ObjectDoesNotExist:
            CartProductORM.objects.create(
                number=cart.product_number[reference],
                cart=CartORM.objects.get(identifier=identifier),
                product=ProductORM.objects.get(reference=reference))
