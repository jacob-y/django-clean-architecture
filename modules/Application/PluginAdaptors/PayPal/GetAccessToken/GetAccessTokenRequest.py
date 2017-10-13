from modules.Application.PluginAdaptors.HTTPMixin import HTTPMixin


class GetAccessTokenRequest(HTTPMixin):
    _client_id: str
    _client_secret: str

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

    def _data(self) -> dict:
        return {'grant_type': 'client_credentials'}

    def _endpoint(self) -> str:
        return 'https://api-m.sandbox.paypal.com/v1/oauth2/token'

    def _method(self) -> str:
        return 'POST'

    def _headers(self) -> dict:
        return {
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }

    def _is_form_encoded(self) -> bool:
        return True

    def _auth(self) -> tuple:
        return self._client_id, self._client_secret
