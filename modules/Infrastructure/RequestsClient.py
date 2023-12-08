import requests
from requests.exceptions import RequestException
from modules.Application.PluginAdaptors.HTTPClientInterface import HTTPClientInterface


class RequestsClient(HTTPClientInterface):
    """
    Very basic implementation of HTTP calls with the requests library.
    May be replaced later be a better library.
    """

    @staticmethod
    def _process_response(response: requests.Response) -> dict:
        try:
            if 200 <= response.status_code < 500:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code} error while calling {response.url}")
        except RequestException as e:
            raise Exception(f"Connection failed while calling {response.url}")

    def get(self, endpoint: str, headers: dict, auth: tuple) -> dict:
        return self._process_response(requests.get(endpoint, headers=headers, auth=auth))

    def post(self, endpoint: str, headers: dict, is_form_encoded: bool, data: dict, auth: tuple) -> dict:
        if is_form_encoded:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            return self._process_response(requests.post(endpoint, data=data, headers=headers, auth=auth))
        return self._process_response(requests.post(endpoint, json=data, headers=headers, auth=auth))
