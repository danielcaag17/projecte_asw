from django.http import JsonResponse
from rest_framework.views import APIView
from django.http import HttpResponse
from django.template import loader


class Endpoint1View(APIView):
    def get(self, request):
        # Example response data
        data = {"message": "Hello World"}
        return JsonResponse(data)


def main(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def new_link(request):
    template = loader.get_template('new_link.html')
    return HttpResponse(template.render())
