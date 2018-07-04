from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Device Name")
    isAlarmEnabled = models.BooleanField(max_length=30, verbose_name="Enabled")