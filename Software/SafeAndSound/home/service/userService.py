from home.models import User
from datetime import datetime


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


def update_user (manage_form, user):
    all_data = dict(manage_form.data)
    if all_data.__contains__('birthDate'):
        try:
            user.birthDate = datetime.strptime(next(iter(all_data['birthDate']), None), '%d/%m/%Y')
        except:
            user.birthDate = user.birthDate

    if all_data.__contains__('email'):
        user.email = next(iter(all_data['email']), None)

    if all_data.__contains__('firstName'):
        user.firstName = next(iter(all_data['firstName']), None)

    if all_data.__contains__('lastName'):
        user.lastName = next(iter(all_data['lastName']), None)

    if all_data.__contains__('phoneNumber'):
        user.phoneNumber = next(iter(all_data['phoneNumber']), None)

    if all_data.__contains__('password'):
        user.password = next(iter(all_data['password']), None)

    return user
