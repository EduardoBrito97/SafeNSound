from django.urls import include, path
from . import views

urlpatterns = [
    path('list', views.list_devices, name='index'),
    path('register', views.register_devices, name='register'),
    path('delete/<int:device_id>', views.delete_device, name='delete'),
    path('edit/<int:device_id>', views.edit, name='edit'),
]