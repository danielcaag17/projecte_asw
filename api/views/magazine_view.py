from kbin.models import Publicacio,Thread,Link
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.serializer_magazines import *

class LlistarMagazines(APIView):

    def get(self, request, ordre):
        magazines = Magazine.objects.all()
        if ordre == 'threads':
            magazine_threads = {}
            for magazine in magazines:
                magazine_threads[magazine.id] = magazine.total_threads()

            magazines = sorted(magazines, key=lambda x: magazine_threads.get(x.id, 0), reverse=True)
            magazines_serializer = MagazineSerializer(magazines, many=True).data

        elif ordre == 'elements':
            magazine_elements = {}
            for magazine in magazines:
                magazine_elements[magazine.id] = magazine.total_publicacions()

            magazines = sorted(magazines, key=lambda x: magazine_elements.get(x.id, 0), reverse=True)
            magazines_serializer = MagazineSerializer(magazines, many=True).data

        elif ordre == 'commented':
            magazine_comments = {}
            for magazine in magazines:
                magazine_comments[magazine.id] = magazine.total_comments()
            magazines = sorted(magazines, key=lambda x: magazine_comments.get(x.id, 0), reverse=True)
            magazines_serializer = MagazineSerializer(magazines, many=True).data

        elif ordre == 'suscriptions':
            magazines_serializer = MagazineSerializer(magazines, many=True).data
            magazines_serializer = sorted(magazines_serializer, key=lambda x: x['n_suscriptions'], reverse=True)

        else: return Response({"Error: La url sol·licitada no existeix"}, status=404)


        return Response(magazines_serializer)


