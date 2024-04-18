from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy

from ..models import *


def sort(all, ordre):
    if ordre == 'top':
        res = sorted(all, key=lambda x: x.num_likes, reverse=True)
    elif ordre == 'newest':
        res = sorted(all, key=lambda x: x.creation_data, reverse=True)
    elif ordre == 'commented':
        res = sorted(all, key=lambda x: x.num_coments, reverse=True)
    return res


def view_user(request, username, ordre=None):
    template = loader.get_template('view_user.html')
    obj = User.objects.get(username=username)
    threads = Publicacio.objects.filter(author=username)
    comments = Comment.objects.filter(author=username)
    links = Link.objects.filter(author=username)

    all = list(threads) + list(comments) + list(links)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted}
    print(all_sorted)
    return HttpResponse(template.render(context, request))


def view_user_threads(request, username, ordre=None):
    template = loader.get_template('view_user.html')    # TODO: Definir template
    obj = User.objects.get(username=username)
    threads = Publicacio.objects.filter(author=username)

    all = list(threads)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted}
    return HttpResponse(template.render(context, request))


def view_user_comments(request, username, ordre=None):
    template = loader.get_template('view_user.html')  # TODO: Definir template
    obj = User.objects.get(username=username)
    comments = Comment.objects.filter(author=username)

    all = list(comments)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted}
    return HttpResponse(template.render(context, request))


def view_user_posts(request, username, ordre=None):
    template = loader.get_template('view_user.html')  # TODO: Definir template
    obj = User.objects.get(username=username)
    posts = Posts.objects.filter(author=username)

    all = list(posts)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted}
    return HttpResponse(template.render(context, request))


def view_user_answers(request, username, ordre=None):
    template = loader.get_template('view_user.html')  # TODO: Definir template
    obj = User.objects.get(username=username)
    answers = Answers.objects.filter(author=username)

    all = list(answers)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted}
    return HttpResponse(template.render(context, request))


def view_user_boosts(request, username, ordre=None):
    template = loader.get_template('view_user.html')  # TODO: Definir template
    obj = User.objects.get(username=username)
    boosts = Boosts.objects.filter(author=username)

    all = list(boosts)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted}
    return HttpResponse(template.render(context, request))


def get_username(user_email):
    return user_email.split('@')[0]


def login(request):
    print("He passat pel login")
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
