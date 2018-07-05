from django.forms import ModelForm
from .models import Device
from django import forms
from .service import deviceService


class DeviceRegister(ModelForm):
    device = forms.ChoiceField(choices=deviceService.get_device_choices())

    class Meta:
        model = Device
        exclude = ['bluetooth_id']

    def __init__(self, *args, **kwargs):
        super(DeviceRegister, self).__init__(*args, **kwargs)
        choices = deviceService.get_device_choices()
        self.fields['device'] = forms.ChoiceField(choices=choices, widget=forms.Select())

    def save(self, commit=True):
        device = Device()
        device.name = self.cleaned_data['name']
        device.bluetooth_id = self.cleaned_data['device']
        device.isAlarmEnabled = self.cleaned_data['isAlarmEnabled']
        device.save()