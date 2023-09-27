from abc import ABC, abstractmethod


class HTTPClientInterface(ABC):

    @abstractmethod
    def get(self, endpoint: str, headers: dict, auth: tuple) -> dict:
        pass

    @abstractmethod
    def post(self, endpoint: str, headers: dict, is_form_encoded: bool, data: dict, auth: tuple) -> dict:
        pass
