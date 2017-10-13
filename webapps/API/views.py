from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.exceptions import NotFound, ValidationError, APIException
from modules.entities.product import NullOrNegativePriceException, InvalidReference, \
    TooManyProductsRemoved
from modules.entities.cart import NullOrNegativeParityException, NullOrNegativeProductAddedException
from modules.usecases.fill_cart import fill_cart
from modules.usecases.fill_available_products import fill_available_products
from modules.presentation.cart import display_cart_json, display_cart_xml
from modules.presentation.product import display_product_json, display_product_xml
from postgres_api.queries import ProductRecords, CartRecords
from http_api.euro_dollar_api import EuroDollarAPI


class HTTPAPIException(APIException):
    status_code = HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Internal API call to euro-dollar API failed'
    default_code = 'Internal API call to euro-dollar API failed'


# replace domain exceptions with web API exceptions
def wrap_exceptions(func):
    def func_(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidReference:
            raise ValidationError('Reference must be composed of capital letter first then numbers')
        except NullOrNegativePriceException:
            raise ValidationError('The price must be a non null positive value')
        except NullOrNegativeParityException:
            raise HTTPAPIException('Error from the euro dollar HTTP API: null or negative value')
        except NullOrNegativeProductAddedException:
            raise ValidationError('Use a positive non null number when adding a product')
        except TooManyProductsRemoved:
            raise ValidationError('There is not enough products in stock to do this')
    return func_


class CartView(APIView):

    @wrap_exceptions
    def get(self, request, identifier):
        euro_dollar_parity = EuroDollarAPI().get_euro_dollar_rate()['rate']
        cart = CartRecords.get_by_identifier(identifier)
        if cart is None:
            raise NotFound(detail='No cart with this identifier')
        display_param = request.query_params.get('display_format', None)
        if display_param == 'xml':
            return Response(display_cart_xml(cart, euro_dollar_parity))
        return Response(display_cart_json(cart, euro_dollar_parity))

    @wrap_exceptions
    def post(self, request, identifier):
        cart = CartRecords.get_by_identifier(identifier)
        if cart is None:
            return Response(display_cart_json(CartRecords.create(identifier)),
                            status=HTTP_201_CREATED)
        else:
            euro_dollar_parity = EuroDollarAPI().get_euro_dollar_rate()['rate']
            return Response(display_cart_json(cart, euro_dollar_parity))


class ProductView(APIView):

    @wrap_exceptions
    def get(self, request, reference):
        product = ProductRecords.get_by_reference(reference)
        if product is None:
            raise NotFound(detail='No product with this reference')
        display_param = request.query_params.get('display_format', None)
        if display_param == 'xml':
            return Response(display_product_xml(product))
        return Response(display_product_json(product))

    @wrap_exceptions
    def post(self, request, reference):
        if 'price' not in request.data.keys():
            raise ValidationError('Price must be specified in POST field')
        product = ProductRecords.get_by_reference(reference)
        if product is None:
            return Response(
                display_product_json(ProductRecords.create(reference, request.data['price'])),
                status=HTTP_201_CREATED)
        else:
            return Response(display_product_json(product))


@api_view(['POST'])
@wrap_exceptions
def fill_cart_view(request, identifier):
    if 'reference' not in request.data.keys():
        raise ValidationError('Product reference is missing')
    if 'number' not in request.data.keys():
        raise ValidationError('Number is missing')
    cart, product = fill_cart(CartRecords.get_by_identifier(identifier),
                              ProductRecords.get_by_reference(request.data['reference']),
                              int(request.data['number']))
    ProductRecords.update(request.data['reference'], product)
    CartRecords.update(identifier, cart, request.data['reference'])
    euro_dollar_parity = EuroDollarAPI().get_euro_dollar_rate()['rate']
    return Response(display_cart_json(cart, euro_dollar_parity))


@api_view(['POST'])
@wrap_exceptions
def add_products(request, reference):
    if 'number' not in request.data.keys():
        raise ValidationError('Number is missing')
    product = fill_available_products(
        ProductRecords.get_by_reference(reference), int(request.data['number']))
    ProductRecords.update(reference, product)
    return Response(display_product_json(product))
