from django.urls import include, path
from . import views

urlpatterns = [
    path('list', views.list_devices, name='index'),
    path('register', views.register_devices, name='register'),

]