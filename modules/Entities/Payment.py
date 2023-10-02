from money import Money
from enum import Enum


class PaymentStatus(Enum):
    SUCCESSFUL = 1
    PENDING = 2
    FAILED = 3
    REFUNDED = 4


class Payment:

    money: Money | None = None # Money is a Value Object that stores the amount & currency
    transaction_id: str | None = None  # ID on our system
    gateway_id: str | None = None  # ID of the payment on PayPal
    capture_id: str | None = None  # ID of the payment capture on PayPal
    return_url: str | None = None  # URL where to redirect the payer from PayPal after the payment
    redirect_url: str | None = None  # URL where to redirect the payer to PayPal to do the payment
    status: PaymentStatus | None = None
    gateway_status: str | None  # status on PayPal
    error_code: str | None = None
    error_message: str | None = None

    def __init__(self, amount: int | None = None, currency: str | None = None, transaction_id: str | None = None,
                 gateway_id: str | None = None, return_url: str | None = None):
        if amount and currency:
            self.money = Money(amount=amount, currency=currency)
        self.transaction_id = transaction_id
        self.gateway_id = gateway_id
        self.return_url = return_url

    def check(self):
        if self.money and 1 < self.money.amount > 10000:
            raise Exception('The amount must be between 1 and 10 000 of the currency unit')

    def to_string(self) -> dict:
        out = {
            'gateway_id': self.gateway_id,
            'status': self.status.name
        }
        if self.gateway_status:
            out['gateway_status'] = self.gateway_status
        if self.redirect_url:
            out['redirect_url'] = self.redirect_url
        if self.status == PaymentStatus.FAILED:
            out['error_code'] = self.error_code
            out['error_message'] = self.error_message
        return out
