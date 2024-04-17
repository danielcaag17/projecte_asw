from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from ..models import User


def view_user(request, username):
    template = loader.get_template('view_user.html')
    obj = User.objects.get(username=username)
    context = {'user': obj}
    # numero amics, numero threads + threads_id, numero comments + comments_id + parents, boost
    # count = Friends.objects.filter(user=username).count()
    return HttpResponse(template.render(context, request))


def get_username(user_email):
    return user_email.split('@')[0]


def login(request):
    user_email = request.user.email
    djando_username = request.user.username
    user_username = get_username(user_email)
    User.objects.get_or_create(
        username=user_username,
        email=user_email,
    )
    if request.user.is_authenticated:
        url = reverse('main') + f'?django_user={djando_username}&user={user_username}'
        return redirect(url)


def edit_user(request, username):
    template = loader.get_template('edit_user.html')
    obj = User.objects.get(username=username)
    context = {'user': obj}
    return HttpResponse(template.render(context, request))


def settings(request, username):
    template = loader.get_template('user_settings.html')
    obj = User.objects.get(username=username)
    context = {'user': obj}
    return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)
    return redirect("/")
