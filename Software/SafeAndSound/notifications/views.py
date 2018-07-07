from django.shortcuts import render
from .models import Notification
from home.service import userService


def list_notifications(request):
    user = userService.get_user_from_request(request)
    new_notifications = list(Notification.objects.filter(user=user, read=False))
    notifications = list(Notification.objects.filter(user=user, read=True))
    context = {'currentUser': user,
               'notifications': notifications,
               'new_notifications': new_notifications,
               }
    for notification in Notification.objects.filter(user=user, read=False):
        notification.read = True
        notification.save()
    return render(request, 'notifications/list.html', context)
