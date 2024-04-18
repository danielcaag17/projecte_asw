from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Value, CharField
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from ..models import *


@csrf_exempt
def sort(all, ordre):
    if ordre == 'top':
        res = sorted(all, key=lambda x: x.num_likes, reverse=True)
    elif ordre == 'newest':
        res = sorted(all, key=lambda x: x.creation_data, reverse=True)
    elif ordre == 'commented':
        res = sorted(all, key=lambda x: x.num_coments, reverse=True)
    return res


@csrf_exempt
def view_user(request, username, ordre=None):
    template = loader.get_template('view_user.html')
    obj = User.objects.get(username=username)
    threads = Publicacio.objects.filter(author=username).annotate(type=Value('thread', output_field=CharField()))
    comments = Comment.objects.filter(author=username).annotate(type=Value('comment', output_field=CharField()))
    links = Link.objects.filter(author=username).annotate(type=Value('link', output_field=CharField()))

    all = list(threads) + list(comments) + list(links)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'usuari': obj, 'all': all_sorted, 'ordre': ordre}
    print(all_sorted)
    return HttpResponse(template.render(context, request))


@csrf_exempt
def view_user_threads(request, username, ordre=None):
    template = loader.get_template('view_user_elements.html')
    obj = User.objects.get(username=username)
    threads = Publicacio.objects.filter(author=username)

    all = list(threads)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted, 'ordre': ordre, 'type': "threads"}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def view_user_comments(request, username, ordre=None):
    template = loader.get_template('view_user_elements.html')
    obj = User.objects.get(username=username)
    comments = Comment.objects.filter(author=username)

    all = list(comments)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted, 'ordre': ordre, 'type': "comments"}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def view_user_boosts(request, username, ordre=None):
    template = loader.get_template('view_user_elements.html')
    obj = User.objects.get(username=username)
    boosts = Boost.objects.filter(user=username)

    all = list(boosts)
    if ordre == '':
        ordre = 'newest'
    all_sorted = sort(all, ordre)
    context = {'user': obj, 'all': all_sorted, 'ordre': ordre, 'type': "boosts"}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def get_username(user_email):
    return user_email.split('@')[0]


@csrf_exempt
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


@csrf_exempt
def edit_user(request, username):
    if request.method == "POST":
        obj = User.objects.get(username=username)
        description = request.POST.get('description')
        if description is not None:
            obj.description = description
        avatar = request.FILES.get('avatar')
        if avatar is not None:
            avatar_name = default_storage.save('avatar/' + avatar.name, avatar)
            obj.avatar = default_storage.url(avatar_name)
        cover = request.FILES.get('cover')
        if cover is not None:
            cover_name = default_storage.save('cover/' + cover.name, cover)
            obj.cover = default_storage.url(cover_name)
        obj.save()
        template = loader.get_template('edit_user.html')
        context = {'usuari': obj}
        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('edit_user.html')
        obj = User.objects.get(username=username)
        context = {'user': obj}
        return HttpResponse(template.render(context, request))


@csrf_exempt
def settings(request):
    template = loader.get_template('user_settings.html')
    # obj = User.objects.get(username=username)
    # context = {'user': obj}
    return HttpResponse(template.render())


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect("/")


