from ..AbstractPayPalRequest import AbstractPayPalRequest


class GetAccessTokenRequest(AbstractPayPalRequest):

    def _data(self) -> dict:
        return {'grant_type': 'client_credentials'}

    def _endpoint(self) -> str:
        return super()._endpoint() + '/v1/oauth2/token'

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
        return (self.paypal_plugin_adaptor.client_id, self.paypal_plugin_adaptor.client_secret)
