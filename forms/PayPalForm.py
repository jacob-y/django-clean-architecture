from django import forms
from forms.PaymentFormMixin import PaymentFormMixin
from modules.Entities.Payment import PaymentMethod


class PayPalForm(PaymentFormMixin):
    payment_method = forms.CharField(label='Payment Method', initial=PaymentMethod.PAYPAL.value,
                                     widget=forms.HiddenInput())
