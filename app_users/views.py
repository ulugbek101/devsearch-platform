from django.shortcuts import render, redirect
from django.contrib import messages, auth

from .forms import UserRegistrationForm


def developers(request):
    return render(request, 'app_users/developers.html')


def user_account(request):
    profile = request.user.profile

    context = {
        'profile': profile,
    }
    return render(request, 'app_users/account.html', context)


def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'Logout first to log in again')
        return redirect('developers')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, f'Welcome, {user.username}')
            return redirect('account')
        else:
            messages.error(request, 'Incorrect credentials, check and try again')
            return redirect('login')

    return render(request, 'app_users/login.html')


def user_registration(request):
    if request.user.is_authenticated:
        messages.info(request, 'Log out first')
        return redirect('developers')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been successfully created')
            return redirect('login')
        else:
            messages.error(request, 'Check and fill the form correctly')
            return redirect('registration')

    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'app_users/registration.html', context)


def user_logout(request):
    auth.logout(request)
    return redirect('login')
