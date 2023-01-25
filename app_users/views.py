from django.shortcuts import render, redirect
from django.contrib import messages, auth


def developers(request):
    return render(request, 'app_users/developers.html')


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
            return redirect('developers')
        else:
            pass

    return render(request, 'app_users/login.html')


def user_logout(request):
    auth.logout(request)
    return redirect('login')
