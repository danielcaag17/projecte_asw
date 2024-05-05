from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.user_serializer import *
from ..serializers.thread_serializer import *
from ..serializers.link_serializer import *


class UserView(APIView):
    def get(self, request, username=None, element=None, ordre=None, filtre=None):
        print(element, ordre, filtre)
        if username:
            return self.retrieve(request, username, element, ordre, filtre)
        else:
            return self.list(request)

    def retrieve(self, request, username, element, ordre, filtre):
        try:
            user = User.objects.get(username=username)
            user_serializer = UserSerializer(user)
            serializer = {}
            if element is None or element == 'threads':
                tot_ordenat = None
                if filtre is None or filtre == 'tot':
                    filtre = 'tot'
                    threads = Thread.objects.filter(author=username)
                    thread_serializer = ThreadSerializer(threads, many=True)

                    links = Link.objects.filter(author=username)
                    link_serializer = LinkSerializer(links, many=True)

                    tot = link_serializer.data + thread_serializer.data
                    try:
                        tot_ordenat = ordena(tot, ordre)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

                elif filtre == 'threads':
                    threads = Thread.objects.filter(author=username)
                    thread_serializer = ThreadSerializer(threads, many=True)
                    try:
                        tot_ordenat = ordena(thread_serializer.data, ordre)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

                elif filtre == 'links':
                    links = Link.objects.filter(author=username)
                    link_serializer = LinkSerializer(links, many=True)
                    try:
                        tot_ordenat = ordena(link_serializer.data, ordre)
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

                else:
                    return Response({"error": f"The filter '{filtre}' does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = {
                    "user": user_serializer.data,
                    filtre: tot_ordenat
                }

            elif element == 'comments':
                pass
            elif element == 'boosts':
                # nomes quan es el mateix user
                pass
            else:
                return Response({"error": f"The element '{element}' does not exist"},
                                status=status.HTTP_404_NOT_FOUND)

            return Response(serializer, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"The user '{username}' does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def ordena(elements, ordre):
    if ordre is None or ordre == 'newest':
        elements = sorted(elements, key=lambda x: x['creation_data'], reverse=True)
    elif ordre == 'top':
        elements = sorted(elements, key=lambda x: x['num_likes'], reverse=True)
    elif ordre == 'commented':
        elements = sorted(elements, key=lambda x: x['num_coments'], reverse=True)
    else:
        raise Exception(f"The order '{ordre}' does not exist")
    return elements
