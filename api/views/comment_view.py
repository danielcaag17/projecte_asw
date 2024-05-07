from kbin.models import Publicacio, Thread, Link, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from ..serializers.comment_serializer import CommentSerializer


class VeureComentarisPublicacio(APIView):
    def get(self, request, id_thread):

        # Obtenim la publicacio
        try:
            publicacio = Publicacio.objects.get(id=id_thread)
        except:
            return Response({"Error: No hi ha cap publicacio amb id {}".format(id_thread)}, status=404)

        # Obtenim els comentaris
        comentaris = Comment.objects.filter(thread=publicacio, level=1)
        comentaris_serializer = CommentSerializer(comentaris, many=True).data
        return Response(comentaris_serializer)
