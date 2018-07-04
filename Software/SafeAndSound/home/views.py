from django.shortcuts import render
from .forms import UserSignUpForm, UserSignInForm, UserManageForm, AddressForm
from .service import userService


def index(request):
    user = userService.get_user_from_request(request)
    context = {'currentUser': user,
               'current_page': 'Safe And Sound'}
    return render(request, 'home/index.html', context)


def login(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)

        if form.is_valid():

            user = form.get_user()
            userService.update_user_session(user, request)
            return index(request)

        else:
            context = {'loginForm': form,
                       'current_page': 'Login'}
            return render(request, 'home/login.html', context)

    else:
        form = UserSignInForm()
        context = {'loginForm': form,
                   'currentUser': userService.get_user_from_request(request),
                   'current_page': 'Login'}
        return render(request, 'home/login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)
        address_form = AddressForm(request.POST)

        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save(commit=False)
            address = address_form.save(commit=False)
            address.save()
            user.address = address
            user.save()
            userService.update_user_session(user, request)
            return index(request)
        else:
            context = {'userRegisterForm': user_form,
                       'addressRegisterForm': address_form,
                       'currentUser': userService.get_user_from_request(request),
                       'current_page': 'Register'}
            return render(request, 'home/register.html', context)

    else:
        user_form = UserSignUpForm()
        address_form: AddressForm = AddressForm()
        context = {'userRegisterForm': user_form,
                   'addressRegisterForm': address_form,
                   'currentUser': userService.get_user_from_request(request),
                   'current_page': 'Register'}
        return render(request, 'home/register.html', context)


def logout(request):
    request.session['currentUsername'] = None
    request.session['currentPassword'] = None
    return index(request)


def manage(request):
    user = userService.get_user_from_request(request)

    if request.method == "POST":
        user_form = UserManageForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = userService.update_user(user_form, user)
            user.address = address_form.save()
            user.save()
            userService.update_user_session(user, request)
            return index(request)
        else:
            context = {'manageAccountForm': user_form,
                       'addressRegisterForm': address_form,
                       'currentUser': user,
                       'current_page': 'Manage Account'}
            return render(request, 'home/manage.html', context)
    else:
        user_form = UserManageForm()
        address_form = AddressForm()
        if user is not None:
            user_form = UserManageForm(instance=user)
            address_form = AddressForm(instance=user.address)
        context = {'currentUser': user,
                   'addressRegisterForm': address_form,
                   'manageAccountForm': user_form,
                   'current_page': 'Manage Account'}
        return render(request, 'home/manage.html', context)
