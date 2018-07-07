from django.db import models
from home.models import User
from devices.models import Device


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    read = models.BooleanField()
    message = models.CharField(max_length=60)

    def __str__(self):
        return self.device.name + " says:" + self.message
