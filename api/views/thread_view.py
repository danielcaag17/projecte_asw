from kbin.models import Publicacio,Thread,Link
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.serializer_threads import *

class LlistaThreadLinks(APIView):
    def get(self, request,filter,ordre):
        # Obtenim publicacions segons filtre:
        if filter == 'threads':
            resultats = Thread.objects.all()
            resultats_serializer = ThreadSerializer(resultats,many=True).data
        elif filter == 'links':
            resultats = Link.objects.all()
            resultats_serializer = LinkSerializer(resultats,many=True).data
        elif filter == 'publicacions':
            threads = Thread.objects.all()
            links = Link.objects.all()
            thread_serializer = ThreadSerializer(threads, many=True)
            link_serializer = LinkSerializer(links, many=True)
            resultats_serializer = thread_serializer.data + link_serializer.data

        if ordre == 'newest':
            tot = sorted(resultats_serializer, key=lambda x: x['creation_data'],reverse=True)
        elif ordre == 'commented':
            tot = sorted(resultats_serializer, key=lambda x: x['num_coments'],reverse=True)
        elif (ordre == 'top'):
            tot = sorted(resultats_serializer, key=lambda x: x['num_likes'],reverse=True)

        return Response(tot)


