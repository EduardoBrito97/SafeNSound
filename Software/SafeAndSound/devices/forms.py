from django.forms import ModelForm
from .models import Device


class DeviceRegister (ModelForm):
    class Meta:
        model = Device
        exclude = []
