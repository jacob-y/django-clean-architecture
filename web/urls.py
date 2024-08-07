"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from webapps.views import (payment_create, payment_capture, payment_status)

urlpatterns = [
    path(r'payment/<str:payment_gateway>/create',
         payment_create, name='Create Payment'),
    path(r'payment/<str:payment_gateway>/<str:payment_id>',
         payment_status, name='Get Payment'),
    path(r'payment/<str:payment_gateway>/<str:payment_id>/capture',
         payment_capture, name='Capture Payment'),
]
