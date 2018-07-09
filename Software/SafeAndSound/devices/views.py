from django.shortcuts import render
from home.service import userService
from .models import Device
from .forms import DeviceRegister, DeviceEdit
from home.views import index


def list_devices(request):
    user = userService.get_user_from_request(request)
    context = {'currentUser': user,
               'current_page': 'List Devices',
               'all_devices': Device.objects.filter(
                   userOwner=user)}
    return render(request, 'devices/list.html', context)


def register_devices(request):
    if request.method == 'POST':
        form = DeviceRegister(request.POST)
        if form.is_valid():
            form.save(user=userService.get_user_from_request(request))
            device_name = form.cleaned_data['name']
            return index(request, message='Device "' + device_name +'" unsynced successfully.')
        else:
            context = {'currentUser': userService.get_user_from_request(request),
                       'current_page': 'Register Device',
                       'device_form': form}
            return render(request, 'devices/device_register.html', context)
    else:
        form = DeviceRegister()
        context = {'currentUser': userService.get_user_from_request(request),
                   'current_page': 'Register Device',
                   'device_form': form}
        return render(request, 'devices/device_register.html', context)


def delete_device(request, device_id):
    try:
        device = Device.objects.get(id=device_id)
        device_name = device.name
        if device.userOwner == userService.get_user_from_request(request):
            Device.objects.get(id=device_id).delete()
        return index(request, message='Device "' + device_name +'" unsynced successfully.')
    except:
        context = {'currentUser': userService.get_user_from_request(request)}
        return render(request, 'devices/device_not_found.html', context)


def edit(request, device_id):
    user = userService.get_user_from_request(request)
    try:
        device = Device.objects.get(id=device_id)
        if request.method == "POST":
            form = DeviceEdit(request.POST)
            if form.is_valid():
                device.name = form.cleaned_data["name"]
                device.isAlarmEnabled = form.cleaned_data["isAlarmEnabled"]
                device.save()
                return index(request)
            else:
                context = {
                    "currentUser": user,
                    "current_page": "Edit Device " + device.name,
                    "device_form": form,
                    "device": device
                }
                return render(request, "devices/edit.html", context)
        else:
            form = DeviceEdit(instance=device)
            context = {
                "currentUser": user,
                "current_page": "Edit Device " + device.name,
                "device_form": form,
                "device": device
            }
            return render(request, "devices/edit.html", context)
    except:
        context = {'currentUser': userService.get_user_from_request(request)}
        return render(request, 'devices/device_not_found.html', context)
