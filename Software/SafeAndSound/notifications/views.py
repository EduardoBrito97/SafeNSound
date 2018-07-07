from django.shortcuts import render
from .models import Notification
from home.service import userService


def list_notifications(request):
    user = userService.get_user_from_request(request)
    context = {'currentUser': user,
               'notifications': Notification.objects.filter(user=user),
               }
    return render(request, 'notifications/list.html', context)
