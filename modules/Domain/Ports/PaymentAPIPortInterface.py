from abc import ABC, abstractmethod
from modules.Entities.Payment import Payment
from modules.Entities.Payer import Payer


class PaymentAPIPort:

    @abstractmethod
    def create_payment(self, data: dict) -> Payment:
        raise NotImplementedError

    @abstractmethod
    def create_payer(self, data: dict) -> Payer:
        raise NotImplementedError

    @abstractmethod
    def get_payment(self, gateway_id: str) -> Payment:
        raise NotImplementedError
