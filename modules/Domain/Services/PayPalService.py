from modules.Domain.Plugins.AbstractPayPalPlugin import PayPalPlugin
from modules.Entities.Payment import Payment, PaymentStatus
from modules.Entities.Payer import Payer


class PayPalService:

    paypal_plugin: PayPalPlugin

    def __init__(self, paypal_plugin: PayPalPlugin):
        self.paypal_plugin = paypal_plugin

    def pay(self, payment: Payment, payer: Payer):
        payment.check()
        self.paypal_plugin.get_access_token()
        self.paypal_plugin.create_order(payment, payer).update_payment()

    def status(self, payment: Payment):
        payment.check()
        self.paypal_plugin.get_access_token()
        self.paypal_plugin.show_order_details(payment).update_payment()

    def capture(self, payment: Payment):
        self.status(payment)
        if payment.status == PaymentStatus.PENDING:
            self.paypal_plugin.capture_payment_for_order(payment).update_payment()
