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


class CrearMagazine(APIView):
    def post(self, request):
        api_key = request.headers.get('Authorization')
        if (api_key == None):
            return Response({"Error: Es necessari indicar el token del usuari"}, status=401)
        data = request.data
        required_fields = {"name", "title"}
        if required_fields.issubset(data.keys()):
            if len(data["name"]) == 0:
                return Response({"error: Nom buit"}, status=400)
            elif len(data["title"]) == 0:
                return Response({"error: Títol buit"}, status=400)
            try:
                usuari = User.objects.get(api_key=api_key)
            except:
                return Response({"Error: el token no correspon amb cap usuari registrat"}, status=403)

            description = data.get("description")
            rules = data.get("rules")
            nsfw = data.get("nsfw")
            nou_magazine = Magazine.objects.create(author=usuari,
                                                   name= data["name"],
                                                   creation_date= timezone.now().isoformat(),
                                                   title=data["title"],
                                                   description=description,
                                                   rules=rules,
                                                   nsfw=nsfw)

            nou_magazine = MagazineSerializer(nou_magazine)
            return Response(nou_magazine.data, status=201)
        else:
            return Response({"Error: Falten atributs. Cal indicar nom i títol de la magazine a crear."},
                            status=400)
