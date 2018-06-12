import datetime
from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="Username", help_text="Your Login Username")
    password = models.CharField(max_length=30, verbose_name="Password")
    birthDate = models.DateField(max_length=30, verbose_name="Birth Date")
    email = models.EmailField(max_length=50, verbose_name="Email")
    firstName = models.CharField(max_length=50, verbose_name="First Name")
    lastName = models.CharField(max_length=50, verbose_name="Last Name")
    phoneNumber = models.CharField(max_length=50, verbose_name="Phone Number", null = True)

    def __str__(self):
    	return self.firstName + ' ' + self.lastName

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    zipCode = models.CharField(max_length=50, verbose_name="Zip Code", default=None, blank=True, null=True)
    street = models.CharField(max_length=50, verbose_name="Street")
    number = models.CharField(max_length=50, verbose_name="Number")
    complement = models.CharField(max_length=50, verbose_name="Complement", default=None, blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name="Country", default=None, blank=True, null=True)

    def __str__(self):
    	return self.street + ',' + self.number