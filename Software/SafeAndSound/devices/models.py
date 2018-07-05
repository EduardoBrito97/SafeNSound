from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=30, verbose_name="Device Name")
    bluetooth_id = models.CharField(max_length=30, unique=True)
    isAlarmEnabled = models.BooleanField(max_length=30, verbose_name="Enabled")

    def __str__(self):
        return self.name + ", id:" + self.bluetooth_id