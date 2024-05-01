from rest_framework import serializers
from kbin.models.thread import *

class Thread_serializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'author','title', 'body', 'creation_data','magazine','num_likes','num_dislikes',
                  'num_boosts','num_coments']

class Link_serializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'author', 'title', 'body', 'creation_data', 'magazine', 'num_likes', 'num_dislikes',
                  'num_boosts','num_coments','url']
