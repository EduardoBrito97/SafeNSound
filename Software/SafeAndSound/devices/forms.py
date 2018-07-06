from django.forms import ModelForm
from .models import Device
from django import forms
from .service import deviceService
from bluetooth import *


class DeviceRegister(ModelForm):
    device = forms.ChoiceField(choices=deviceService.get_device_choices())
    password = forms.CharField(max_length=30, label='Bluetooth PIN', required=False)

    class Meta:
        model = Device
        exclude = ['bluetooth_id', 'userOwner']

    def __init__(self, *args, **kwargs):
        super(DeviceRegister, self).__init__(*args, **kwargs)
        choices = deviceService.get_device_choices()
        self.fields['device'] = forms.ChoiceField(choices=choices, widget=forms.Select())

    def clean_device(self):
        try:
            device = Device.objects.get(bluetooth_id=self.cleaned_data['device'])
            self.add_error('device', 'Device already registered.')

        except:
            try:
                services = find_service(address=self.cleaned_data['device'],
                                        uuid=SERIAL_PORT_CLASS)
                for i in range(len(services)):
                    match = services[i]
                    if match["host"] == self.cleaned_data['device']:
                        break
                port = match["port"]
                s = BluetoothSocket(RFCOMM)
                s.connect((self.cleaned_data['device'], port))
                return self.cleaned_data["password"]
            except:
                self.add_error("password", "Wrong pin.")
            return self.cleaned_data['device']

    def save(self, commit=True, user=None):
        device = Device()
        device.name = self.cleaned_data['name']
        device.bluetooth_id = self.cleaned_data['device']
        device.isAlarmEnabled = self.cleaned_data['isAlarmEnabled']
        device.userOwner = user
        if user is not None:
            device.save()
