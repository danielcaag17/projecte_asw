from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.user_serializer import *
from ..serializers.thread_serializer import *


class UserView(APIView):
    def get(self, request, username=None):
        if username:
            return self.retrieve(request, username)
        else:
            return self.list(request)

    def retrieve(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"The user '{username}' does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserThreadsView(APIView):
    def get(self, request, username=None):
        try:
            user = User.objects.get(username=username)
            threads = Thread.objects.filter(author=username)

            user_serializer = UserSerializer(user)
            thread_serializer = ThreadSerializer(threads, many=True)
            serializer = {
                "user": user_serializer.data,
                "threads": thread_serializer.data
            }
            return Response(serializer, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"The user '{username}' does not exist"},
                            status=status.HTTP_404_NOT_FOUND)