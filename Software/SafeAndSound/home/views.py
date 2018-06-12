from django.shortcuts import render
from .forms import UserSignUpForm, UserSignInForm
from .service import userService


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
                context = {'currentUser': user}
                userService.update_user_session(user, request)
                return render(request, 'home/index.html', context)

            else:
                form = UserSignInForm()
                context = {'loginForm': form}
                return render(request, 'home/login.html', context)

        else:
            context = {'loginForm': form}
            return render(request, 'home/login.html', context)

    else:
        form = UserSignInForm()
        context = {'loginForm': form,
                   'User': userService.get_user_from_request(request)}
        return render(request, 'home/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            userService.update_user_session(user, request)
            context = {'currentUser': user}
            return render(request, 'home/index.html', context)
        else:
            context = {'currentUser': form}
            return render(request, 'home/register.html', context)

    else:
        form = UserSignUpForm()
        context = {'currentUser': form}
        return render(request, 'home/register.html', context)


def logout(request):
    request.session['currentUsername'] = None
    request.session['currentPassword'] = None
    context = {'currentUser': None}
    return render(request, 'home/index.html', context)
