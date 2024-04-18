from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy
from itertools import chain

from ..models import *




def view_user(request, username, filter=None,ordre=None,select='threads'):
    template = loader.get_template('view_user.html')
    obj = User.objects.get(username=username)
    links_tot = Link.objects.filter(author_id=username)
    threads_tot = Thread.objects.filter(author_id=username)
    comments = Comment.objects.filter(author_id=username)
    boosts = Boost.objects.filter(user_id=username)

    nboosts =len(boosts)
    print(nboosts)
    nthreads = len(list(links_tot)+list(threads_tot))
    ncom = len(comments)
    if select == 'threads':


        context = {'usuari': obj, 'threads': ordena(links_tot,threads_tot,ordre,filter),
                   'active_option': ordre, 'active_filter': filter, 'selected': select,
                   'n_threads' : nthreads,'n_com' : ncom,'n_boosts' : nboosts}

    elif select == 'com':

        if ordre == 'top':
            comments = sorted(comments, key=lambda x: x.num_likes, reverse=True)
        elif ordre == 'newest':
            comments = sorted(comments, key=lambda x: x.creation_data, reverse=True)
        else:
            comments = sorted(comments, key=lambda x: x.creation_data, reverse=False)

        thread_ids = [comment.thread_id for comment in comments]

        links = Link.objects.filter(id__in=thread_ids)
        threads = Thread.objects.filter(id__in=thread_ids)

        publicacions = sorted(chain(links, threads), key=lambda x: thread_ids.index(x.id))

        parella = [(commen, publicacion) for commen, publicacion in
                                          zip(comments, publicacions)]


        context = {'usuari': obj, 'coments': comments, 'active_option': ordre, 'active_filter': filter,
                   'selected': select,'pare':parella,'n_threads' : nthreads,'n_com' : ncom,'n_boosts' : nboosts}

    else:

        publication_ids = boosts.values_list('publicacio_id', flat=True)

        links = Link.objects.filter(id__in=publication_ids)
        threads = Thread.objects.filter(id__in=publication_ids)

        context = {'usuari': obj, 'threads': ordena(links,threads,ordre,filter), 'active_option': ordre,
                   'active_filter': filter, 'selected': select,'n_threads' : nthreads,'n_com' : ncom,'n_boosts' : nboosts}

    return HttpResponse(template.render(context, request))



def ordena(links,threads,ordre,filter):
    if filter == 'links':
        tot = links
    elif filter == 'threads':
        tot = threads
    else:
        tot = list(links) + list(threads)

    if ordre == 'top':
        tot = sorted(tot, key=lambda x: x.num_likes, reverse=True)
    elif ordre == 'newest':
        tot = sorted(tot, key=lambda x: x.creation_data, reverse=True)
    elif ordre == 'commented':
        tot = sorted(tot, key=lambda x: x.num_coments, reverse=True)
    return tot




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
