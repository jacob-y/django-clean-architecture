from abc import ABC, abstractmethod


class Configuration(ABC):

    @abstractmethod
    def get_paypal_client_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_paypal_client_secret(self) -> str:
        raise NotImplementedError
