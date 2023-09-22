from abc import ABC, abstractmethod
import requests
from requests.exceptions import RequestException
from modules.Entities import Payment
from modules.Entities.Payer import Payer
import json


class AbstractPayPalRequest(ABC):
    # typing set up with a string to avoid circular dependency
    # between AbstractRequest children classes & PayPalPluginAdaptor
    paypal_plugin_adaptor: 'PayPalPluginAdaptor'
    _payment: Payment = None
    _payer: Payer = None

    def __init__(self, paypal_plugin_adapator: 'PayPalPluginAdaptor', payment: Payment = None, payer: Payer = None):
        self.paypal_plugin_adaptor = paypal_plugin_adapator
        self._payment = payment
        self._payer = payer

    @abstractmethod
    def _data(self) -> dict:
        return {}

    def _headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.paypal_plugin_adaptor.access_token}',
            'Prefer': 'return=representation'
        }

    @abstractmethod
    def _endpoint(self) -> str:
        return 'https://api-m.sandbox.paypal.com'

    @abstractmethod
    def _method(self) -> str:
        return 'GET'

    def _is_form_encoded(self) -> bool:
        return False

    def _auth(self) -> tuple | None:
        return None

    def send(self) -> dict:
        """
        Very basic implementation of HTTP calls with the requests library.
        May be replaced later by an interface and an adaptor to allow to change the HTTP client.
        """
        try:

            headers = self._headers()
            match self._method():
                case 'GET':
                    response = requests.get(self._endpoint(), headers=headers)
                case 'POST':
                    if self._is_form_encoded():
                        headers['Content-Type'] = 'application/x-www-form-urlencoded'
                        response = requests.post(self._endpoint(), data=self._data(), headers=headers,
                                                 auth=self._auth())
                    else:
                        response = requests.post(self._endpoint(), json=self._data(), headers=headers,
                                                 auth=self._auth())
                case _:
                    raise Exception(f'Unsupported HTTP method {self._method()}')

            if 200 <= response.status_code < 500:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code} error while calling {self._endpoint()}")

        except RequestException as e:
            raise Exception(f"Connection failed while calling {self._endpoint()}")
