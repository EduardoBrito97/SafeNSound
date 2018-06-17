from django.shortcuts import render
from .forms import UserSignUpForm, UserSignInForm, UserManageForm
from .service import userService
from datetime import datetime


# Create your views here.
def index(request):
    user = userService.get_user_from_request(request)
    context = {'currentUser': user}
    return render(request, 'home/index.html', context)


def login(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)

        if form.is_valid():
            currentUsername = form.cleaned_data['username']
            currentPassword = form.cleaned_data['password']
            user = userService.find_user_by_username_and_password(currentUsername, currentPassword)

            if user is not None:
                userService.update_user_session(user, request)
                return index(request)

            else:
                form.add_error('username', 'Username e/ou password não está(ão) correto(s)')
                context = {'loginForm': form}
                return render(request, 'home/login.html', context)

        else:
            context = {'loginForm': form}
            return render(request, 'home/login.html', context)

    else:
        form = UserSignInForm()
        context = {'loginForm': form,
                   'currentUser': userService.get_user_from_request(request)}
        return render(request, 'home/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            userService.update_user_session(user, request)
            return index(request)
        else:
            form = UserSignUpForm()
            context = {'userRegisterForm': form}
            return render(request, 'home/register.html', context)

    else:
        form = UserSignUpForm()
        context = {'userRegisterForm': form,
                   'currentUser': userService.get_user_from_request(request)}
        return render(request, 'home/register.html', context)


def logout(request):
    request.session['currentUsername'] = None
    request.session['currentPassword'] = None
    return index(request)


def manage(request):
    user = userService.get_user_from_request(request)

    if request.method == "POST":
        form = UserManageForm(request.POST)
        if form.is_valid():
            try:
                datetime.strptime(form.data['birthDate'], '%d/%m/%Y')
                if user.password != form.data['password'] and form.data['password'] != form.data['confirmPassword']:
                    form.add_error('confirmPassword', 'Passwords não são iguais')
            except:
                form.add_error('birthDate', 'Data em formato errado (DD/MM/YYYY)')
                context = {'manageAccountForm': form,
                           'currentUser': user}
                if user.password != form.data['password'] and form.data['password'] != form.data['confirmPassword']:
                    form.add_error('confirmPassword', 'Passwords não são iguais')
                return render(request, 'home/manage.html', context)
            user = userService.update_user(form, user)
            user.save()
            userService.update_user_session(user, request)
            return index(request)

        else:
            context = {'manageAccountForm': form,
                       'currentUser': user}
            return render(request, 'home/manage.html', context)
    else:
        form = UserManageForm()
        if user is not None:
            form = UserManageForm(instance=user)
        context = {'currentUser': user,
                   'manageAccountForm': form}
        return render(request, 'home/manage.html', context)
