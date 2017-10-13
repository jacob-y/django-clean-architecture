# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^cart/(?P<identifier>\w+)/$',
        views.CartView.as_view(), name='cart'),
    url(r'^cart/(?P<identifier>\w+)/add/$',
        views.fill_cart_view, name='fill cart'),
    url(r'^product/(?P<reference>\w+)/$',
        views.ProductView.as_view(), name='product'),
    url(r'^product/(?P<reference>\w+)/add/$',
        views.add_products, name='add products'),
]
