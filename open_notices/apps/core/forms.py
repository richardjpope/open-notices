from django import forms
from django.conf import settings
from core import models

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'password', 'display_name']

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user