from rest_framework import serializers
from kbin.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'description', 'cover', 'avatar', 'email']
