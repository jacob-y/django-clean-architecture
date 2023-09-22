from django import forms


class PaymentFormMixin(forms.Form):
    email = forms.EmailField(label='Email', initial='john.doe@example.com')
    first_name = forms.CharField(label='First Name', initial='John')
    last_name = forms.CharField(label='Last Name', initial='Doe')
    address1 = forms.CharField(label='Address 1', initial='1 rue des roses')
    address2 = forms.CharField(label='Address 2', initial='2nd étage')
    postcode = forms.CharField(label='Postcode', initial='44000')
    city = forms.CharField(label='City', initial='Nantes')
    country_code = forms.CharField(label='Country Code', initial='FR')
    amount = forms.FloatField(label='Amount', initial=10.)
