from django import forms

class InputForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=50)
    lastname = forms.CharField(label='Last Name', max_length=50)
    rollnumber = forms.IntegerField(label='Roll Number')    
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # input_text = forms.CharField(label='Input Text', max_length=100)