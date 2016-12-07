from django import forms
from django.conf import settings
from core import models

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'password', 'display_name']

    password = forms.CharField(label='Password', widget=forms.PasswordInput)