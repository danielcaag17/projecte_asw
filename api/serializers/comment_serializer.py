from rest_framework import serializers
from kbin.models import Comment, Thread, Link


class CommentSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # TODO: Cal posar el level?
        # Field 'parent' necessari per quan es mostren els comentaris d'un user
        fields = ['author', 'body', 'creation_data', 'last_edited', 'num_likes', 'num_dislikes',
                  'level', 'thread', 'parent']

    def get_parent(self, obj):
        base = "http://127.0.0.1:8000/api/"
        if Thread.objects.filter(id=obj.thread_id).exists():
            base += "threads/" + str(obj.thread_id) + "/"
        elif Link.objects.filter(id=obj.thread_id).exists():
            base += "links/" + str(obj.thread_id) + "/"

        return base
