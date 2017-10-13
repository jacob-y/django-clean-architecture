from modules.Domain.Plugins.AbstractStripePlugin import StripePlugin
from modules.Entities.Payment import Payment, PaymentStatus, PaymentMethod
from modules.Entities.Payer import Payer


class StripeService:

    stripe_plugin: StripePlugin

    def __init__(self, stripe_plugin: StripePlugin):
        self.stripe_plugin = stripe_plugin

    def pay(self, payment: Payment, payer: Payer):
        payment.check([PaymentMethod.CARD, PaymentMethod.SEPA_DIRECT_DEBIT])

        if payment.payment_method == PaymentMethod.CARD:
            # the card token must have been pre-saved on Stripe
            # (for instance with the Stripe Elements JS library)
            payment.gateway_id = payment.card.token
            self.stripe_plugin.retrieve_payment_method(payment).update_payment()
        else:
            self.stripe_plugin.create_payment_method(payment, payer).update_payment()

        if payment.status == PaymentStatus.PENDING:
            self.stripe_plugin.create_payment_intent(payment, payer).update_payment()

    def status(self, payment: Payment):
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
