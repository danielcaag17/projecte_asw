from rest_framework import serializers
from kbin.models.user import User


class UserSerializer(serializers.ModelSerializer):
    total_threads = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    total_boosts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'description', 'cover', 'avatar', 'email',
                  'total_threads', 'total_comments', 'total_boosts']

    def get_total_threads(self, obj):
        return obj.total_threads

    def get_total_comments(self, obj):
        return obj.total_comments

    def get_total_boosts(self, obj):
        return obj.total_boosts

