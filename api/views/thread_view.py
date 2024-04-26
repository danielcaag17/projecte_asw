from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView

from kbin.models import Publicacio
from rest_framework.response import Response


class PublicacioTitleListView(APIView):
    def get(self, request):
        titles = list(Publicacio.objects.values_list('title', flat=True))
        return JsonResponse({'titles': titles})
