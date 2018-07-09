from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.list_notifications, name='list'),
    path('delete/', views.clean_notifications, name='delete'),
]