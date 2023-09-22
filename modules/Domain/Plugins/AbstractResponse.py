from abc import ABC
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod


class AbstractResponse(ABC):

    _data: dict = None
    _payment: Payment = None

    def __init__(self, data: dict, payment: Payment = None):
        self._data = data
        self._payment = payment

    def update_payment(self):
        """Safe update of the payment that avoids erasing values with None (when the result is not implemented)."""
        self._payment.gateway_id = self.payment_id() or self._payment.gateway_id
        self._payment.gateway_status = self.gateway_status() or self._payment.gateway_status
        self._payment.capture_id = self.capture_id() or self._payment.capture_id
        self._payment.redirect_url = self.redirect_url() or self._payment.redirect_url
        self._payment.error_code = self.error_code() or self._payment.error_code
        self._payment.error_message = self.error_message() or self._payment.error_message
        self._payment.payment_method = self.payment_method() or self._payment.payment_method
        # Update the payment status
        if self.is_successful():
            self._payment.status = PaymentStatus.SUCCESSFUL
        elif self.is_refunded():
            self._payment.status = PaymentStatus.REFUNDED
        elif self.is_pending():
            self._payment.status = PaymentStatus.PENDING
        elif self.is_failed():
            self._payment.status = PaymentStatus.FAILED

    # ERRORS
    """
    The error message returned by the payment gateway.
    To be overridden by the child class.
    """
    def error_message(self) -> str | None:
        return None

    """
    The error code returned by the payment gateway.
    To be overridden by the child class.
    """
    def error_code(self) -> str | None:
        return None

    # PAYMENT STATUS
    """
    If the payment was successful.
    To be overridden by the child class.
    """
    def is_successful(self) -> bool:
        return False

    """
    If the payment is pending.
    To be overridden by the child class.
    """
    def is_pending(self) -> bool:
        return False

    """
    If the payment was refunded.
    To be overridden by the child class.
    """
    def is_refunded(self) -> bool:
        return False

    """
    If the payment was refunded.
    To be overridden by the child class.
    """
    def is_failed(self) -> bool:
        return False

    """
    The raw status on the payment gateway.
    To be overridden by the child class.
    """
    def gateway_status(self) -> str | None:
        return None

    # REDIRECTION
    """
    The URL to redirect the user to.
    To be overridden by the child class.
    """
    def redirect_url(self) -> str | None:
        return None

    # PAYMENT INFORMATION
    """
    The ID of the payment on the payment gateway.
    To be overridden by the child class.
    """
    def payment_id(self) -> str | None:
        return None

    """
    The ID of the capture on the payment gateway.
    To be overridden by the child class.
    """
    def capture_id(self) -> str | None:
        return None

    """
    The payment method used.
    To be overridden by the child class.
    """
    def payment_method(self) -> PaymentMethod | None:
        return None
