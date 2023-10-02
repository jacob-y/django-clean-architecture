from modules.Domain.Plugins.AbstractPayPalPlugin import PayPalPlugin
from modules.Entities import Payment
from modules.Entities.Payer import Payer


class PayPalService:

    paypal_plugin: PayPalPlugin

    def __init__(self, paypal_plugin: PayPalPlugin):
        self.paypal_plugin = paypal_plugin

    def pay(self, payment: Payment, payer: Payer):
        payment.check()
        self.paypal_plugin.get_access_token()
        self.paypal_plugin.create_order(payment, payer)

    def status(self, payment: Payment):
        payment.check()
        self.paypal_plugin.get_access_token()
        self.paypal_plugin.show_order_details(payment)

    def capture(self, payment: Payment):
        payment.check()
        self.paypal_plugin.get_access_token()
        self.paypal_plugin.capture_payment_for_order(payment)

    def refund(self, payment: Payment):
        self.status(payment)
        if payment.status == Payment.PaymentStatus.SUCCESSFUL:
            self.paypal_plugin.refund_captured_payment(payment)
