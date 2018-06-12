from django.forms import ModelForm
from django import forms
from .models import User


class UserSignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'birthDate', 'email', 'firstName', 'lastName', 'phoneNumber']


class UserSignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
