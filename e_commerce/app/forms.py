from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

payment_choices=(
    ('G','Googlepay'),('P','Phonepay'),('A','Amazonpay'),('C','Cash on Delivery')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2= forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    shipping_zip = forms.CharField(required=False)

    billing_address=forms.CharField(required=False)
    billing_address2= forms.CharField(required=False)
    billing_country=CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(attrs={'class':'custom-select d-block w-100',}))

    billing_zip=forms.CharField(required=False)

    same_billing_address=forms.BooleanField(required=False)
    set_default_shipping=forms.BooleanField(required=False)
    use_default_shipping=forms.BooleanField(required=False)
    set_default_billing= forms.BooleanField(required=False)
    use_default_billing=forms.BooleanField(required=False)

    payment_options=forms.ChoiceField(widget=forms.RadioSelect,
    choices=payment_choices)


class CouponForm(forms.Form):
    pass

class RefundForm(forms.Form):
    pass

class PaymentForm(forms.Form):
    pass




