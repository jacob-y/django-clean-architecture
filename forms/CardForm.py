from forms.PaymentFormMixin import PaymentFormMixin
from django import forms
from modules.Entities.Payment import PaymentMethod


class CardForm(PaymentFormMixin):
    number = forms.CharField(label='Card Number', required=True, initial='4242424242424242')
    expiry_month = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 13)], required=True, initial='12')
    expiry_year = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(24, 30)],
                                    required=True, initial='2024')
    cvv = forms.CharField(label='Card CVV', required=True, initial='123')
    brand = forms.ChoiceField(choices=[('Visa', 'Visa'), ('Mastercard', 'Mastercard')],
                              required=True, initial='Visa')
    payment_method = forms.CharField(label='Payment Method', initial=PaymentMethod.CARD.value,
                                     widget=forms.HiddenInput())
