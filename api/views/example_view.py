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


def main(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def new_link(request):
    template = loader.get_template('new_link.html')
    return HttpResponse(template.render())

@csrf_exempt #todo: PREGUNTAR PK NO SURT BE SENSE AIXO!
def create_link(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')

        if body == '':
            body = None
        user_prova, _ = User.objects.get_or_create(
            username='default_user',  # Aquí defines el nom d'usuari desitjat
            email='example@example.com',  # Defineix una adreça de correu electrònic
            password="default_password",  # Defineix una contrasenya (criptografiada)
          #  register_date=timezone.now().isoformat()  # Defineix una data de registre
        )

        # Creem una nova instància del model Thread amb les dades proporcionades
        link = Thread.objects.create(
            title=title,
            body=body,
            url=url,
            author=user_prova
        )

        # Un cop s'ha creat el fil de discussió, redirigeix l'usuari a alguna altra pàgina
        return redirect('main')
    else:
        # Si la petició no és POST, simplement mostrem el formulari
        return redirect('/new')

