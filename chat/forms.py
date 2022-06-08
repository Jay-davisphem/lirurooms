from django import forms


class UsernameForm(forms.Form):
    unique_name = forms.CharField(label="Your username", max_length=100)
