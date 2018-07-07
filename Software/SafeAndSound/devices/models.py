from django.db import models
from home.models import User


class Device(models.Model):
    name = models.CharField(max_length=30, verbose_name="Device Name")
    bluetooth_id = models.CharField(max_length=100, unique=True)
    isAlarmEnabled = models.BooleanField(max_length=30, verbose_name="Enabled")
    userOwner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ", id:" + self.bluetooth_id