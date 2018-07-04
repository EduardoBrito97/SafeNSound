from django.forms import ModelForm
from django import forms
from .models import User, Address
from datetime import datetime


class UserSignUpForm(ModelForm):
    confirmPassword = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type': 'password'}), required=True,
                                      label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'password', 'birthDate', 'email', 'firstName', 'lastName', 'phoneNumber']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
            'birthDate': forms.DateTimeInput(format='%d/%m/%Y')
        }

    def clean_birthDate(self):
        birth_date = self.cleaned_data['birthDate']
        if birth_date >= datetime.now().date():
            self.add_error('birthDate', 'Date can not be in the future')
        return birth_date

    def clean_confirmPassword(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirmPassword']
        if password != confirm_password:
            self.add_error('confirmPassword', 'Passwords must match')
        return confirm_password


class UserSignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type': 'password'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            self.add_error('username', "Username or password do not match")

    def get_user(self):
        return User.objects.get(username=self.cleaned_data['username'], password=self.cleaned_data['password'])


class UserManageForm(ModelForm):
    confirmPassword = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'type': 'password'}), required=False,
                                      label="Confirm password")

    class Meta:
        model = User
        exclude = ['username', 'address']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
            'birthDate': forms.DateTimeInput(format='%d/%m/%Y')
        }

    def clean_birthDate(self):
        birth_date = self.cleaned_data['birthDate']
        if birth_date >= datetime.now().date():
            self.add_error('birthDate', 'Date can not be in the future')
        return birth_date

    def clean_confirmPassword(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirmPassword']

        if (confirm_password is not None and password != confirm_password) and not not confirm_password:
            self.add_error('confirmPassword', 'Password must match')
        return confirm_password


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = []
