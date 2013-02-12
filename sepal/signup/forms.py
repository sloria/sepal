from django import forms
from django.core.mail import send_mail

class SignupForm(forms.Form):
    email = forms.EmailField()