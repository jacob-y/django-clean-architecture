from abc import ABC, abstractmethod
from modules.Entities.Payment import Payment, PaymentStatus


class AbstractResponse(ABC):

    _data: dict = None
    _payment: Payment = None

    def __init__(self, data: dict, payment: Payment = None):
        self._data = data
        self._payment = payment

    def update_payment(self):
        """Safe update of the payment that avoids erasing values with None."""
        self._payment.gateway_id = self.id() or self._payment.gateway_id
        self._payment.gateway_status = self.status()
        self._payment.capture_id = self.capture_id() or self._payment.capture_id
        self._payment.redirect_url = self.redirect_url() or self._payment.redirect_url
        self._payment.error_code = self.error_code() or self._payment.error_code
        self._payment.error_message = self.error_message() or self._payment.error_message
        if self.is_successful():
            self._payment.status = PaymentStatus.SUCCESSFUL
        elif self.is_refunded():
            self._payment.status = PaymentStatus.REFUNDED
        elif self.is_pending():
            self._payment.status = PaymentStatus.PENDING
        else:
            self._payment.status = PaymentStatus.FAILED

    @abstractmethod
    def error_message(self) -> str | None:
        return None

    @abstractmethod
    def error_code(self) -> str | None:
        return None

    @abstractmethod
    def is_successful(self) -> bool:
        return False

    @abstractmethod
    def is_pending(self) -> bool:
        return False

    @abstractmethod
    def is_refunded(self) -> bool:
        return False

    @abstractmethod
    def redirect_url(self) -> str | None:
        return None

    @abstractmethod
    def id(self) -> str | None:
        return None

    @abstractmethod
    def capture_id(self) -> str | None:
        return None

    @abstractmethod
    def status(self) -> str | None:
        return None
