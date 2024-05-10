from kbin.models import Publicacio, Thread, Link, Comment, User, Reply
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from ..serializers.comment_serializer import CommentSerializer


class VeureComentarisPublicacio(APIView):
    def get(self, request, id_thread):
        try:
            publicacio = Publicacio.objects.get(id=id_thread)
        except:
            return Response({"Error: No hi ha cap publicacio amb id {}".format(id_thread)}, status=404)

        comentaris = Comment.objects.filter(thread=publicacio, level=1)
        comentaris_serializer = CommentSerializer(comentaris, many=True).data
        return Response(comentaris_serializer)

class CrearComentari(APIView):
    def post(self, request, id_thread):
        api_key = request.headers.get('Authorization')
        if api_key is None:
            return Response({"Error: Es necessari indicar el token de l'usuari"}, status=401)

        try:
            publicacio = Publicacio.objects.get(id=id_thread)
        except:
            return Response({"Error: No hi ha cap publicacio amb id {}".format(id_thread)}, status=404)

        body = request.data.get('body')
        if not body:
            return Response({"Error: Falta el body del comentari"}, status=400)

        try:
            usuari = User.objects.get(api_key=api_key)
        except:
            return Response({"Error: El token no correspon amb cap usuari registrat"}, status=403)

        comment = Comment.objects.create(author=usuari, thread=publicacio, body=body, level=1)
        comment.save()

        comment = CommentSerializer(comment)
        return Response(comment.data, status=201)


class CrearComentariResposta(APIView):
    def post(self, request, id_comment):
        api_key = request.headers.get('Authorization')
        if api_key is None:
            return Response({"Error: Es necessari indicar el token de l'usuari"}, status=401)

        try:
            comentari_root = Comment.objects.get(id=id_comment)
        except:
            return Response(
                {"Error": "No hi ha cap comentari amb id {}".format(id_comment)},
                status=404)

        body = request.data.get('body')
        if not body:
            return Response({"Error: Falta el body del comentari resposta"}, status=400)

        try:
            usuari = User.objects.get(api_key=api_key)
        except:
            return Response({"Error: el token no correspon amb cap usuari registrat"}, status=403)

        # Creem el comentari
        comment = Comment.objects.create(author=usuari, thread=comentari_root.thread, body=body,
                                         level=comentari_root.level + 1)
        comment.save()

        reply = Reply.objects.create(comment_root=comentari_root, comment_reply=comment)
        reply.save()

        comentari_root = CommentSerializer(comentari_root)

        # Retorna el comentari origen perque es vegi que s'ha creat la resposta
        return Response(comentari_root.data, status=201)
