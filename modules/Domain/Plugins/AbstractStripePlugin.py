from abc import ABC, abstractmethod
from modules.Entities import Payment
from modules.Entities.Payer import Payer
from modules.Domain.Plugins.AbstractResponse import AbstractResponse


class StripePlugin(ABC):

    secret_key: str
    access_token: str | None = None

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    @abstractmethod
    def create_payment_intent(self, payment: Payment, payer: Payer) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def create_payment_method(self, payment: Payment, payer: Payer) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def retrieve_payment_intent(self, payment: Payment) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def retrieve_charge(self, payment: Payment) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def retrieve_payment_method(self, payment: Payment) -> AbstractResponse:
        raise NotImplementedError
