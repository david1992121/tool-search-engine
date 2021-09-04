from user.models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

def file_validator(file):
    max_file_size = 1024 * 1024 * 5

    if file.size > max_file_size:
        raise serializers.ValidationError(_('Max file size is {} and your file size is {}'.
            format(max_file_size, file.size)))
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

class AvatarSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar', )
