from home.models import User


def update_user_session(user, request):
    request.session['currentUsername'] = user.username
    request.session['currentPassword'] = user.password


def get_user_from_request(request):
    current_username = request.session.get('currentUsername')
    current_password = request.session.get('currentPassword')

    return find_user_by_username_and_password(current_username, current_password)


def find_user_by_username_and_password(current_username, current_password):
    try:
        user = User.objects.get(username=current_username, password=current_password)
    except User.DoesNotExist:
        user = None
    return user
