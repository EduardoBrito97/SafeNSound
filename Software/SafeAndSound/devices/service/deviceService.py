from bluetooth import *


def get_device_choices():
    nearby_devices = discover_devices(lookup_names=True)
    return tuple(nearby_devices)
