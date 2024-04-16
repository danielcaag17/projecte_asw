from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from ..models import User


def view_user(request):
    template = loader.get_template('view_user.html')
    return HttpResponse(template.render())


def get_username(user_email):
    return user_email.split('@')[0]


def login(request):
    user_email = request.user.email
    user_username = get_username(user_email)
    User.objects.get_or_create(
        username=user_username,
        email=user_email,
    )
    if request.user.is_authenticated:
        url = reverse('main') + f'?ordre=""&filter=""&username={user_username}'
        return redirect(url)


def edit_user(request):
    template = loader.get_template('edit_user.html')
    return HttpResponse(template.render())


def settings(request):
    template = loader.get_template('user_settings.html')
    return HttpResponse(template.render())


def logout_view(request):
    logout(request)
    return redirect("/")
