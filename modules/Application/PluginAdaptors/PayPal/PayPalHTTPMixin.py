from modules.Application.PluginAdaptors.HTTPMixin import HTTPMixin
from abc import ABC


class PayPalHTTPMixin(HTTPMixin, ABC):

    _access_token: str

    def _headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._access_token}',
            'Prefer': 'return=representation'
        }

    @staticmethod
    def _url() -> str:
        return 'https://api-m.sandbox.paypal.com'  # only the sandbox is implemented

    def _is_form_encoded(self) -> bool:
        return False

    def _auth(self) -> tuple | None:
        return None
