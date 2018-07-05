from django.shortcuts import render
from home.service import userService
from .models import Device
from .forms import DeviceRegister
from home.views import index


def list_devices(request):
    context = {'currentUser': userService.get_user_from_request(request),
               'current_page': 'List Devices', #current_page dá o título da página e também deixa o link na barra de cima selecionado
               'all_devices': Device.objects.all()}  #Device.objects.all retorna todos os Devices cadastrados
    return render(request, 'devices/list.html', context)


def register_devices(request):
    if request.method == 'POST':
        form = DeviceRegister(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            context = {'currentUser': userService.get_user_from_request(request),
                       'current_page': 'Register Device', # current_page dá o título da página e também deixa o link na barra de cima selecionado
                       'device_form': form}  # DeviceRegister cria um novo form de Device
            return render(request, 'devices/device_register.html', context)
    else:
        form = DeviceRegister()
        context = {'currentUser': userService.get_user_from_request(request),
                   'current_page': 'Register Device', #current_page dá o título da página e também deixa o link na barra de cima selecionado
                   'device_form': form}  #DeviceRegister cria um novo form de Device
        return render(request, 'devices/device_register.html', context)
