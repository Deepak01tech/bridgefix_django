from django import forms

class InputForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    age = forms.IntegerField(label='Age')
    roll_number = forms.CharField(label='Roll Number', max_length=20)
    
