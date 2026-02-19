from django import forms

class ContactForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    # name = forms.CharField(max_length=100)
    # email = forms.EmailField()
    # message = forms.CharField(widget=forms.Textarea)