from abc import ABC, abstractmethod
from modules.Entities import Payment
from modules.Entities.Payer import Payer


class AbstractPayPalRequest(ABC):
    # typing set up with a string to avoid circular dependency
    # between AbstractRequest children classes & PayPalPluginAdaptor
    paypal_plugin_adaptor: 'PayPalPluginAdaptor'
    _payment: Payment = None
    _payer: Payer = None

    def __init__(
            self,
            paypal_plugin_adapator: 'PayPalPluginAdaptor',
            payment: Payment = None,
            payer: Payer = None,
    ):
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
        http_client = self.paypal_plugin_adaptor.http_client_interface
        match self._method():
            case 'GET':
                return http_client.get(
                    self._endpoint(), headers=self._headers(), auth=self._auth())
            case 'POST':
                return http_client.post(
                    self._endpoint(), headers=self._headers(), auth=self._auth(),
                    data=self._data(), is_form_encoded=self._is_form_encoded())
            case _:
                raise Exception(f'Unsupported HTTP method {self._method()}')
