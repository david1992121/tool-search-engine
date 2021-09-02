from user.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length= 5, min_length=5)
    name = serializers.CharField(max_length= 50)

    class Meta:
        fields = ('id', 'name', 'avatar')
        model = User
        extra_kwargs = {
            'avatar': { 'required': False }
        }

class LoginSerializer(serializers.Serializer):
    user = UserSerializer
    token = serializers.CharField()
