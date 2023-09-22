from modules.Domain.Plugins.AbstractStripePlugin import StripePlugin
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer


class StripeService:

    stripe_plugin: StripePlugin

    def __init__(self, stripe_plugin: StripePlugin):
        self.stripe_plugin = stripe_plugin

    def pay(self, payment: Payment, payer: Payer):
        payment.check()
        if payment.payment_method == PaymentMethod.CARD:
            # In test environment we use a predefined payment method
            # Because Stripe does not allow card numbers for non PCI-DSS customers
            payment.gateway_id = 'pm_card_visa'
            self.stripe_plugin.retrieve_payment_method(payment).update_payment()
        else:
            self.stripe_plugin.create_payment_method(payment, payer).update_payment()
        if payment.status == PaymentStatus.PENDING:
            self.stripe_plugin.create_payment_intent(payment, payer).update_payment()

    def status(self, payment: Payment):
        payment.check()
        prefix = payment.gateway_id[:2]
        match prefix:
            case 'pi':
                self.stripe_plugin.retrieve_payment_intent(payment).update_payment()
            case 'ch':
                self.stripe_plugin.retrieve_charge(payment).update_payment()
            case 'pm':
                self.stripe_plugin.retrieve_payment_method(payment).update_payment()
            case '_':
                raise Exception('Unknown Stripe object type.')

    def capture(self, payment: Payment):
        self.status(payment)
