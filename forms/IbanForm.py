from forms.PaymentFormMixin import PaymentFormMixin
from django import forms
from modules.Entities.Payment import PaymentMethod


class IbanForm(PaymentFormMixin):
    iban = forms.CharField(label='IBAN', required=True)
    bic = forms.CharField(label='BIC', required=True)
    payment_method = forms.CharField(label='Payment Method', initial=PaymentMethod.SEPA_DIRECT_DEBIT.value,
                                     widget=forms.HiddenInput())
