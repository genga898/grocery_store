from crispy_forms.helper import FormHelper
from django import forms
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    phone_regex = forms.RegexField(
        regex='^(?:\+254|0)?((?:011[2-5]|07[0-29]|074[0-3,5-6,8]|075[7-9]|076[8-9]|079)\d{6}|1(?:[1-9]\d{6}|0[1-9]\d{5}))$',
        max_length=15
    )
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class MpesaPaymentForm(forms.Form):
    phone_number = forms.CharField(
        validators=[RegexValidator('^(?:\+254|0)?((?:011[0-9]{2}|07[0-29]|074[0-3,5-6,8]|075[7-9]|076[8-9]|079)\d{6}|1(?:[1-9]\d{6}|0[1-9]\d{5}))$')],
        max_length=15
    )
