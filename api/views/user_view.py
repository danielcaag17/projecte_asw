from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.user_serializer import *
from ..serializers.thread_serializer import *


class UserView(APIView):
    def get(self, request, username=None, element=None, ordre=None, filtre=None):
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
                threads = Thread.objects.filter(author=username)
                threads_ordenats = ordena(threads, ordre)
                thread_serializer = ThreadSerializer(threads_ordenats, many=True)
                # thread_serializer = ThreadSerializer(threads, many=True)
                serializer = {
                    "user": user_serializer.data,
                    "threads": thread_serializer.data
                }
                pass
            elif element == 'comments':
                pass
            elif element == 'boosts':
                # mateix user
                pass
            else:
                # error
                pass

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
        elements = sorted(elements, key=lambda x: x.creation_data, reverse=True)
    if ordre == 'top':
        elements = sorted(elements, key=lambda x: x.num_likes, reverse=True)
    elif ordre == 'commented':
        elements = sorted(elements, key=lambda x: x.num_coments, reverse=True)
    else:
        # error
        pass
    return elements
