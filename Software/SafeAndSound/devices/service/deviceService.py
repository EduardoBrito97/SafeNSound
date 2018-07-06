from bluetooth import *


def get_device_choices():
    nearby_devices = discover_devices(lookup_names=True)
    new_tuple = [(devices[0], devices[0]) for devices in nearby_devices]
    return new_tuple
