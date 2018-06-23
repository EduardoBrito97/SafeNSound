from django.shortcuts import render
from .forms import UserSignUpForm, UserSignInForm, UserManageForm
from .service import userService


def index(request):
    user = userService.get_user_from_request(request)
    context = {'currentUser': user}
    return render(request, 'home/index.html', context)


def login(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)

        if form.is_valid():
            user = form.get_user()
            userService.update_user_session(user, request)
            return index(request)

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
