from .models import Notification
from home.views import *

def list_notifications(request):
    user = userService.get_user_from_request(request)
    new_notifications = list(Notification.objects.filter(user=user, read=False))
    notifications = list(Notification.objects.filter(user=user, read=True))
    context = {'currentUser': user,
               'notifications': notifications,
               'new_notifications': new_notifications,
               'current_page': 'News'
               }
    for notification in Notification.objects.filter(user=user, read=False):
        notification.read = True
        notification.save()
    return render(request, 'notifications/list.html', context)


def clean_notifications(request):
    user = userService.get_user_from_request(request)
    user_notifications = Notification.objects.filter(user=user)
    user_notifications.delete()
    return index(request, "Notifications cleaned successfully!")
