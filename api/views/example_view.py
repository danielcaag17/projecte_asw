from django.http import JsonResponse
from rest_framework.views import APIView


class Endpoint1View(APIView):
    def get(self, request):
        # Example response data
        data = {"message": "Hello World"}
        return JsonResponse(data)