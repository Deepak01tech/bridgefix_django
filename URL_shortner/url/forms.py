from django import forms

class UrlForm(forms.Form):
    url= forms.CharField(label='Enter URL', max_length=200)