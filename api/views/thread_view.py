from kbin.models import Publicacio,Thread,Link, Vot
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.serializer_threads import *
import json

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

class CrearThread(APIView):
    def get(self,request): #TODO: CAL?
        #Obtenim els threads
        threads = Thread.objects.all()
        thread_serializer = sorted(ThreadSerializer(threads, many=True).data,key=lambda x: x['creation_data'],reverse=True)
        return Response(thread_serializer)

    def post(self,request):
        api_key = request.headers.get('Authorization')
        if (api_key == None):
            return Response({"Error: Es necessari indicar el token del usuari"}, status=401)
        data = request.data
        required_fields = {"title", "magazine"}
        if required_fields.issubset(data.keys()):
            if len(data["title"]) == 0:
                return Response({"error: Titol buit"}, status=400)

            try: #Comprovem si el magazine indicat existeix
                magazine = Magazine.objects.get(name=data["magazine"])
            except:
                return Response({"Error: No hi ha un magazine amb nom {}".format(data["magazine"])}, status=400)

            try:
                usuari = User.objects.get(api_key=api_key)
            except:
                return Response({"Error: el token no correspon amb cap usuari registrat"}, status=403)

            body = data.get("body")

            nou_thread = Thread.objects.create(author=usuari,title=data["title"], body=body, magazine=magazine)
            nou_thread = ThreadSerializer(nou_thread)
            return Response(nou_thread.data, status=201)  # 201: Created
        else:
            # Si los campos no coinciden, retornamos un error
            return Response({"Error: Falten atributs. Cal indicar titol i magazine del thread a crear."},
                            status=400)  # 400: Bad Request


class CrearLink(APIView):
    def get(self,request): #TODO: CAL?
        #Obtenim els threads
        links = Link.objects.all()
        link_serializer = sorted(ThreadSerializer(links, many=True).data,key=lambda x: x['creation_data'],reverse=True)
        return Response(link_serializer)

    def post(self,request):
        api_key = request.headers.get('Authorization')
        if (api_key == None):
            return Response({"Error: Es necessari indicar el token del usuari"}, status=401)

        data = request.data
        required_fields = {"title", "magazine","url"}
        if required_fields.issubset(data.keys()):
            if len(data["title"]) == 0:
                return Response({"Error: Titol buit"}, status=400)

            if (len(data["url"]) == 0):
                return Response({"Error: URL no indicada"},status=400)

            try: #Comprovem si el magazine indicat existeix
                magazine = Magazine.objects.get(name=data["magazine"])
            except:
                return Response({"Error: No hi ha un magazine amb nom {}".format(data["magazine"])}, status=400)

            try:
                usuari = User.objects.get(api_key=api_key)
            except:
                return Response({"Error: el token no correspon amb cap usuari registrat"}, status=403)

            body = data.get("body")

            nou_link = Link.objects.create(author=usuari,title=data["title"], body=body,
                                             magazine=magazine,url=data["url"])


            nou_link = LinkSerializer(nou_link)
            return Response(nou_link.data, status=201)  # 201: Created
        else:
            # Si los campos no coinciden, retornamos un error
            return Response({"Error: Falten atributs. Cal indicar titol,magazine i url del link a crear."},
                            status=400)  # 400: Bad Request

class LikePublicacion(APIView):
    def post(self,request,IDPublicacio):
        api_key = request.headers.get('Authorization')
        if (api_key == None):
            return Response({"Error: Es necessari indicar el token del usuari"}, status=401)
        try:
            usuari = User.objects.get(api_key=api_key)
        except:
            return Response({"Error: el token no correspon amb cap usuari registrat"}, status=403)

        try:
            publicacio = Publicacio.objects.get(pk=IDPublicacio)
        except:
            return Response({"Error: la publicació no existeix"}, status=404)


        if Vot.objects.filter(user=usuari, publicacio=publicacio).exists(): #L'usuari ja ha votat
            vot = Vot.objects.get(user=usuari, publicacio=publicacio)
            if (vot.positiu):  # Si el vot ja era positiu no fem res i retornem la informació del Thread o el Link
                return self.retorna_info(IDPublicacio)

            else: #Si el vot era negatiu canviem el sentit del vot
                publicacio.num_dislikes -= 1
                publicacio.num_likes += 1
                vot.positiu = True
                vot.save()
                return self.retorna_info(IDPublicacio)

        else: #Creem un nou vot
            nou_vot = Vot(user=usuari, publicacio=publicacio, positiu=True)
            publicacio.num_likes += 1
            publicacio.save()
            nou_vot.save()
            return self.retorna_info(IDPublicacio)


    def retorna_info(self,IDPublicacio):
        try:
            thread = Thread.objects.get(pk=IDPublicacio)
            thread = ThreadSerializer(thread)
            return Response(thread.data, status=200)
        except:
            link = Link.objects.get(pk=IDPublicacio)
            link = LinkSerializer(link)
            return Response(link.data, status=200)


