from abc import ABC, abstractmethod
from modules.Entities import Payment
from modules.Entities.Payer import Payer
from modules.Domain.Plugins.AbstractResponse import AbstractResponse


class PayPalPlugin(ABC):

    client_id: str
    client_secret: str
    access_token: str | None = None

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    def get_access_token(self) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def create_order(self, payment: Payment, payer: Payer) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def capture_payment_for_order(self, payment: Payment) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def refund_captured_payment(self, payment: Payment) -> AbstractResponse:
        raise NotImplementedError

    @abstractmethod
    def show_order_details(self, payment: Payment) -> AbstractResponse:
        raise NotImplementedError
