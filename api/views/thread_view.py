from django.db.models import Q

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
        else:
            return Response({"Error: No existeix el filtre {}".format(filter)}, status=404)

        if ordre == 'newest':
            tot = sorted(resultats_serializer, key=lambda x: x['creation_data'],reverse=True)
        elif ordre == 'commented':
            tot = sorted(resultats_serializer, key=lambda x: x['num_coments'],reverse=True)
        elif (ordre == 'top'):
            tot = sorted(resultats_serializer, key=lambda x: x['num_likes'],reverse=True)
        else:
            return Response({"Error: No existeix l'ordre {}".format(ordre)}, status=404)

        return Response(tot)

class CrearThread(APIView):
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

class VotarPublicacio(APIView):
    def post(self,request,id_publicacio,tipus_vot):
        validacio = self.validar_request(request, id_publicacio, tipus_vot)
        if isinstance(validacio, Response):
            return validacio
        usuari, publicacio = validacio

        if Vot.objects.filter(user=usuari, publicacio=publicacio).exists(): #L'usuari ja ha votat
            vot = Vot.objects.get(user=usuari, publicacio=publicacio)
            if (tipus_vot == 'like'):
                if (vot.positiu):  # Si el vot ja era positiu no fem res i retornem la informació del Thread o el Link
                    return retorna_info_publicacio(id_publicacio)

                else: #Si el vot era negatiu canviem el sentit del vot
                    publicacio.num_dislikes -= 1
                    publicacio.num_likes += 1
                    vot.positiu = True
                    vot.save()
                    publicacio.save()
                    return retorna_info_publicacio(id_publicacio)

            else:
                if (not vot.positiu):  # Si el vot ja era negatiu no fem res i retornem la informació del Thread o el Link
                    return retorna_info_publicacio(id_publicacio)

                else: #Si el vot era positiu canviem el sentit del vot
                    publicacio.num_dislikes += 1
                    publicacio.num_likes -= 1
                    vot.positiu = False
                    vot.save()
                    publicacio.save()
                    return retorna_info_publicacio(id_publicacio)
        else: #Creem un nou vot
            nou_vot = Vot(user=usuari, publicacio=publicacio, positiu= tipus_vot == "like")
            publicacio.num_likes += tipus_vot == "like"
            publicacio.num_dislikes += tipus_vot == "dislike"
            publicacio.save()
            nou_vot.save()
            return retorna_info_publicacio(id_publicacio)

    def delete(self,request,id_publicacio,tipus_vot):
        validacio = self.validar_request(request, id_publicacio, tipus_vot)
        if isinstance(validacio, Response):
            return validacio
        usuari, publicacio = validacio

        if Vot.objects.filter(user=usuari, publicacio=publicacio).exists():  # L'usuari ha votat la publicacio indicada
            vot = Vot.objects.get(user=usuari, publicacio=publicacio)
            if ((tipus_vot == 'like' and vot.positiu) or (tipus_vot == 'dislike' and not vot.positiu)):
                vot.delete()
                publicacio.num_likes -= tipus_vot == 'like'
                publicacio.num_dislikes -= tipus_vot == 'dislike'
                publicacio.save()
                return Response({"Vot eliminat correctament"}, status=204)

            else:
                return Response({"El tipus de vot indicat i el del vot ja existent no coincideixen"},status=400)

        else: #L'usuari encara no ha votat
            return Response({"L'usuari indicat no ha votat la publicació amb ID {}".format(id_publicacio)}, status=404)

    def validar_request(self, request, id_publicacio, tipus_vot):
        api_key = request.headers.get('Authorization')
        if api_key is None:
            return Response({"Error: Es necessari indicar el token del usuari"}, status=401)

        if tipus_vot not in ["like", "dislike"]:
            return Response({"Error: El tipus de vot ha de ser like o dislike"}, status=400)

        try:
            usuari = User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            return Response({"Error: el token no correspon amb cap usuari registrat"}, status=403)

        try:
            publicacio = Publicacio.objects.get(pk=id_publicacio)
        except Publicacio.DoesNotExist:
            return Response({"Error: no hi ha cap publicació amb ID {}".format(id_publicacio)}, status=404)

        return usuari, publicacio








class CercarPublicacions(APIView):
    def get(self, request,filter,ordre):
        keyword = request.headers.get('keyword')

        if (all(char.isspace() for char in keyword)): #Només s'han introduït espais en blanc
            return Response({"La keyword de la cerca no pot ser només espais en blanc"}, status=400)

        # Busquem totes les publicacions que contenen en el titol i el cos la keyword indicada
        links = Link.objects.filter(Q(title__contains=keyword) | Q(body__contains=keyword))
        threads = Thread.objects.filter(Q(title__contains=keyword) | Q(body__contains=keyword))

        thread_serializer = ThreadSerializer(threads, many=True)
        link_serializer = LinkSerializer(links, many=True)

        if filter == 'links':
            resultats_serializer = LinkSerializer(links,many=True).data
        elif filter == 'threads':
            resultats_serializer = ThreadSerializer(threads, many=True).data
        elif filter == 'publicacions':
            resultats_serializer = thread_serializer.data + link_serializer.data
        else:
            return Response({"Error: No existeix el filtre {}".format(filter)}, status=404)


        if ordre == 'newest':
            tot = sorted(resultats_serializer, key=lambda x: x['creation_data'], reverse=True)
        elif ordre == 'commented':
            tot = sorted(resultats_serializer, key=lambda x: x['num_coments'], reverse=True)
        elif (ordre == 'top'):
            tot = sorted(resultats_serializer, key=lambda x: x['num_likes'], reverse=True)
        else:
            return Response({"Error: No existeix l'ordre {}".format(ordre)}, status=404)

        return Response(tot)


class ObtenirPublilcacio(APIView):
    def get(self, request,id_publicacio):
        if Publicacio.objects.filter(pk=id_publicacio).exists():
            return retorna_info_publicacio(id_publicacio)
        else:
            return Response({"Error: No existeix una publicació amb ID {}".format(id_publicacio)}, status=404)

def retorna_info_publicacio(IDPublicacio):
    try:
        thread = Thread.objects.get(pk=IDPublicacio)
        thread = ThreadSerializer(thread)
        return Response(thread.data, status=200)
    except:
        link = Link.objects.get(pk=IDPublicacio)
        link = LinkSerializer(link)
        return Response(link.data, status=200)