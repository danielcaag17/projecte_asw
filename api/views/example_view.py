from django.http import JsonResponse
from rest_framework.views import APIView
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


class Endpoint1View(APIView):
    def get(self, request):
        # Example respeñonse data
        data = {"message": "Hello World"}
        return JsonResponse(data)



def main_list(request,ordre=None,filter=None):
    links = Link.objects.all()
    threads = Thread.objects.all()
    if ordre == '': ordre = 'newest'

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

    context = {'threads': tot, 'active_option': ordre,'active_filter':filter}
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))



def new_link(request):
    template = loader.get_template('new_link.html')
    return HttpResponse(template.render())

def new_thread(request):
    template = loader.get_template('new_thread.html')
    return HttpResponse(template.render())

@csrf_exempt  # todo: PREGUNTAR PK NO SURT BE SENSE AIXO!
def create_link_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')
        created_at = timezone.now().isoformat()

        if body == '':
            body = None
        user_prova, _ = User.objects.get_or_create(
            username='default_user',  # Aquí defines el nom d'usuari desitjat
            email='example@example.com',  # Defineix una adreça de correu electrònic
            password="default_password",  # Defineix una contrasenya (criptografiada)
        )

        # Creem una nova instància del model Thread o Link amb les dades proporcionades
        if url == None:
            thread = Thread.objects.create(
                title=title,
                body=body,
                author=user_prova,
                creation_data=created_at
            )
        else:
            link = Link.objects.create(
                title=title,
                body=body,
                url=url,
                author=user_prova,
                creation_data=created_at
            )

        # Un cop s'ha creat el fil de discussió, redirigeix l'usuari a alguna altra pàgina
        return redirect('main')
    else:
        # Si la petició no és POST, simplement mostrem el formulari
        return redirect('/new')

@csrf_exempt
def like_thread(request,thread_id):
    if request.method == 'POST':
        thread = Publicacio.objects.get(pk=thread_id)
        thread.num_likes += 1
        thread.save()
        next = request.POST.get('next', '/')
        return redirect(next)
    else:
        return redirect('main')

@csrf_exempt
def dislike_thread(request,thread_id):
    if request.method == 'POST':
        thread = Publicacio.objects.get(pk=thread_id)
        thread.num_dislikes += 1
        thread.save()
        next = request.POST.get('next', '/')
        return redirect(next)
    else:
        return redirect('main')

@csrf_exempt
def boost_thread(request,thread_id):
    if request.method == 'POST':
        thread = Publicacio.objects.get(pk=thread_id)
        thread.num_boosts += 1
        thread.save()
        next = request.POST.get('next', '/')
        return redirect(next)
    else:
        return redirect('main')


def veure_thread(request, thread_id):
    thread = Publicacio.objects.get(pk=thread_id)
    comments_root = Comment.objects.filter(thread_id=thread_id, level=1)
    replies = Reply.objects.filter(comment_root__in=comments_root)
    context = {'thread': thread, 'comments_root': comments_root, 'replies': replies}
    #   template = loader.get_template('veure_thread.html')
    return render(request, 'veure_thread.html', context)


@csrf_exempt
def add_comment(request, thread_id):
    print(f"Valor de thread_id: {thread_id}")
    thread = Publicacio.objects.get(pk=thread_id)
    if request.method == 'POST':
        body = request.POST.get('entry_comment[body]')
        if body:
            default_user = User.objects.get(username='default_user')
            comment = Comment(body=body, author=default_user, thread=thread, creation_data=timezone.now())
            comment.save()
    return redirect('veure_thread', thread_id=thread_id)


@csrf_exempt
def add_reply(request, thread_id, comment_id):
    comment_root = Comment.objects.get(pk=comment_id)
    thread = Publicacio.objects.get(pk=thread_id)
    if request.method == 'POST':
        body = request.POST.get('entry_comment[body]')
        if body:
            default_user = User.objects.get(username='default_user')
            comment_reply = Comment(body=body, author=default_user, thread=thread, creation_data=timezone.now(),
                              level=comment_root.level + 1)
            comment_reply.save()
            reply = Reply(comment_root=comment_root, comment_reply=comment_reply)
            reply.save()
    return redirect('veure_thread', thread_id=thread.id)
