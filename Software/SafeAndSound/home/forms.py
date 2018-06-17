from django.forms import ModelForm
from django import forms
from .models import User, Address


class UserSignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'birthDate', 'email', 'firstName', 'lastName', 'phoneNumber']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }


class UserSignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type': 'password'}))


class UserManageForm(ModelForm):
    confirmPassword = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type': 'password'}), required=False, label="Confirm password")

    class Meta:
        model = User
        exclude = ['username', 'Address']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['street']
