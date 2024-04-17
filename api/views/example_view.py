from django.http import JsonResponse
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser

class Endpoint1View(APIView):
    def get(self, request):
        # Example respeñonse data
        data = {"message": "Hello World"}
        return JsonResponse(data)


def main_list(request, ordre=None, filter=None):
    links = Link.objects.all()
    threads = Thread.objects.all()
    user = request.GET.get('user')
    django_username = request.GET.get('django_user')
    djangoUser = {}
    if user is not None and django_username is not None:
        djangoUser = {
            'user': DjangoUser.objects.get(username=django_username),
            'username': user,
        }
        print(djangoUser)

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

    context = {'threads': tot, 'active_option': ordre, 'active_filter': filter, 'user': djangoUser}
    print(context)
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

def all_magazines(request, ordre=None):
    magazines = Magazine.objects.all()
    if ordre == 'threads':
        magazines = sorted(magazines, key=lambda x: x.n_threads, reverse=True)
    elif ordre == 'elements':
        magazines = sorted(magazines, key=lambda x: x.n_elements, reverse=True)
    elif ordre == 'commented':
        magazines = sorted(magazines, key=lambda x: x.n_comments, reverse=True)
    elif ordre == 'suscriptions':
        magazines = sorted(magazines, key=lambda x: x.n_suscriptions, reverse=True)


    context = {'magazines': magazines}

    template = loader.get_template("all_magazines.html")
    return HttpResponse(template.render(context, request))

def new_link(request):
    magazines = Magazine.objects.all()
    context = {'magazines': magazines}
    template = loader.get_template('new_link.html')
    return HttpResponse(template.render(context,request))





@csrf_exempt
def new_magazine(request):
    if request.method == 'POST':

        name = request.POST.get('name')

        author_email = request.user.email
        author = User.objects.get(email=author_email)
        creation_date = timezone.now().isoformat()
        title = request.POST.get('title')
        description = request.POST.get('description')
        rules = request.POST.get('rules')
        nsfw = request.POST.get('isAdult')

        magazine = Magazine.objects.create(
            name=name,
            author=author,
            creation_date=creation_date,
            title=title,
            description=description,
            rules=rules,
            nsfw=nsfw
        )

        return redirect('main')
    else:
        template = loader.get_template("new_magazine.html")
        return HttpResponse(template.render())


def new_thread(request):
    magazines = Magazine.objects.all()
    context = {'magazines': magazines}
    template = loader.get_template('new_thread.html')
    return HttpResponse(template.render(context,request))


@csrf_exempt  # todo: PREGUNTAR PK NO SURT BE SENSE AIXO!
def create_link_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')
        magazine = Magazine.objects.get(id=request.POST.get('magazine'))
        created_at = timezone.now().isoformat()

        if body == '':
            body = None
        author_email = request.user.email
        user = User.objects.get(email=author_email)

        # Creem una nova instància del model Thread o Link amb les dades proporcionades
        if url == None:
            thread = Thread.objects.create(
                title=title,
                body=body,
                author=user,
                magazine=magazine,
                creation_data=created_at,
            )
        else:
            if url.startswith("https://"):
                url = url[len("https://"):]
            elif url.startswith("http://"):
                url = url[len("http://"):]

            if not url.startswith("www."):
                url = f"www.{url}"
            url = url.strip('/')
            link = Link.objects.create(
                title=title,
                body=body,
                url=url,
                author=user,
                magazine=magazine,
                creation_data=created_at
            )

        # Un cop s'ha creat el fil de discussió, redirigeix l'usuari a alguna altra pàgina
        return redirect('main')
    else:
        # Si la petició no és POST, simplement mostrem el formulari
        return redirect('/new')

@csrf_exempt
def boost_thread(request, thread_id):
    if request.method == 'POST':
        thread = Publicacio.objects.get(pk=thread_id)
        thread.num_boosts += 1
        thread.save()
        next = url_redireccio(request)
        return HttpResponseRedirect(next)

    else:
        return redirect('main')


def veure_thread(request, thread_id, order):
    thread = Publicacio.objects.get(pk=thread_id)

    if order == 'newest':
        comments_root = Comment.objects.filter(thread_id=thread_id, level=1).order_by('-creation_data')
    elif order == 'oldest':
        comments_root = Comment.objects.filter(thread_id=thread_id, level=1).order_by('creation_data')
    else:
        comments_root = Comment.objects.filter(thread_id=thread_id, level=1).order_by('-num_likes')
    replies = Reply.objects.filter(comment_root__in=comments_root)
    context = {'thread': thread, 'comments_root': comments_root, 'replies': replies}
    request.session['order'] = order
    return render(request, 'veure_thread.html', context)


def veure_magazine(request, magazine_id, ordre=None, filter=None):

    magazine = Magazine.objects.get(pk=magazine_id)
    links = Link.objects.filter(magazine_id=magazine_id)
    threads = Thread.objects.filter(magazine_id=magazine_id)

    if filter == 'links':
        tot = links
    elif filter == 'threads':
        tot = threads
    else :
        tot = list(links) + list(threads)

    if ordre == 'top':
        tot = sorted(tot, key=lambda x: x.num_likes, reverse=True)
    elif ordre == 'newest':
        tot = sorted(tot, key=lambda x: x.creation_data, reverse=True)
    elif ordre == 'commented':
        tot = sorted(tot, key=lambda x: x.num_coments, reverse=True)

    context = {'magazine': magazine, 'threads': tot}
    return render(request, 'veure_magazine.html', context)


def url_redireccio(request):
    next = request.POST.get('next', '/')
    if 'cercador' in next:
        keyword = request.POST.get('keyword', '')
        next = "{}?keyword={}".format(next, keyword)
    return next
