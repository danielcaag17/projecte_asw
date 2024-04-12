from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.db.models import Q
from ..models import *


def view_cercador(request):
    template = loader.get_template('cercador.html')
    return HttpResponse(template.render())


def cercar(request):
    keyword = request.GET.get('keyword')
    publicacions = sorted(list(Link.objects.filter(Q(title__contains=keyword) | Q(body__contains=keyword)))
                    + list(Thread.objects.filter(Q(title__contains=keyword) | Q(body__contains=keyword))), key=lambda x: x.creation_data, reverse=True)

    context = {'threads': publicacions, 'es_cerca': True, 'num_publicacions': len(publicacions)}

    template = loader.get_template('cercador.html')
    return HttpResponse(template.render(context, request))
