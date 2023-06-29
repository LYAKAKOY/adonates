from django.shortcuts import render, redirect
from social_django.utils import psa


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'users/html/login.html')


def greet(request):
    return render(request, 'users/html/greet_page.html')


@psa('social:complete')
def logout_social(request):
    request.backend.logout(request.user)
    return redirect('/')
