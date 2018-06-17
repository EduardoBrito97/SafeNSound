import datetime
from django.db import models
from django.utils import timezone
from django import forms


class User(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="Username")
    password = models.CharField(max_length=30, verbose_name="Password")
    birthDate = models.DateField(max_length=30, verbose_name="Birth Date")
    email = models.EmailField(max_length=50, verbose_name="Email")
    firstName = models.CharField(max_length=50, verbose_name="First Name")
    lastName = models.CharField(max_length=50, verbose_name="Last Name")
    phoneNumber = models.CharField(max_length=50, verbose_name="Phone Number", null=True)
    Address = models.ForeignKey('Address',
                                on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName


class Address(models.Model):
    User = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    zipCode = models.CharField(max_length=50, verbose_name="Zip Code", default=None, blank=True, null=True)
    street = models.CharField(max_length=50, verbose_name="Street", null=True)
    number = models.CharField(max_length=50, verbose_name="Number", null=True)
    complement = models.CharField(max_length=50, verbose_name="Complement", default=None, blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name="Country", default=None, blank=True, null=True)

    def __str__(self):
        return self.street + ',' + self.number
