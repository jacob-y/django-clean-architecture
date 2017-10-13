from money import Money
from enum import Enum
from modules.Entities.Card import Card
from modules.Entities.Iban import Iban


class PaymentStatus(str, Enum):
    SUCCESSFUL = 'successful'
    PENDING = 'pending'
    FAILED = 'failed'
    REFUNDED = 'refunded'


class PaymentMethod(str, Enum):
    CARD = 'card'
    SEPA_DIRECT_DEBIT = 'sepa'
    PAYPAL = 'paypal'


class Payment:

    money: Money | None = None  # Money is a Value Object that stores the amount & currency
    transaction_id: str | None = None  # ID on our system
    gateway_id: str | None = None  # ID of the payment on the gateway
    capture_id: str | None = None  # ID of the payment capture on the gateway
    redirect_url: str | None = None  # gateway URL where to redirect the payer to do the payment
    return_url: str | None = None  # our URL where to redirect the payer after the payment
    payment_method: PaymentMethod | None = None
    status: PaymentStatus | None = None
    gateway_status: str | None = None  # status on the gateway
    error_code: str | None = None
    error_message: str | None = None
    card: Card | None = None
    iban: Iban | None = None

    def __init__(
            self,
            amount: int | None = None,
            currency: str | None = None,
            transaction_id: str | None = None,
            gateway_id: str | None = None,
            return_url: str | None = None,
            payment_method: PaymentMethod | None = None,
            card: Card | None = None,
            iban: Iban | None = None
    ):
        if amount and currency:
            self.money = Money(amount=amount, currency=currency)
        self.transaction_id = transaction_id
        self.gateway_id = gateway_id
        self.return_url = return_url
        self.payment_method = payment_method
        self.card = card
        self.iban = iban

    def check(self, allowed_payment_methods: list[PaymentMethod]):
        if self.money and 1 < self.money.amount > 10000:
            raise Exception('The amount must be between 1 and 10 000 of the currency unit')
        if self.payment_method == PaymentMethod.CARD and self.card and not self.card.is_valid():
            raise Exception('The card data is invalid')
        if self.payment_method not in allowed_payment_methods:
            raise Exception('The payment method is not allowed in this context')

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
        if self.card:
            out['card'] = {
                'last_4_numbers': self.card.last_4_numbers,
                'expiry_date': self.card.get_expiry_date(),
                'brand': self.card.brand
            }
        if self.iban:
            out['iban'] = {
                'iban': self.iban.iban,
                'bic': self.iban.bic
            }
        return out
