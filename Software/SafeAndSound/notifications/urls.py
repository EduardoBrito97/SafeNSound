from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.list_notifications, name='list'),

]