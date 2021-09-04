from user.serializers import AvatarSerialzer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from .models import User, Token
from django.conf import settings
import random, string, os

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    従業員番号でログイン
    """
    user_id = request.data.get('user_id', "")
    if user_id != "":
        try:
            user = User.objects.get(id=user_id)
            token, created = Token.objects.get_or_create(user=user) 
            if created:
                token.token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
                token.save()

            return Response({"token": token.token, "data": UserSerializer(user).data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    従業員番号で登録
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data.get('id', "")
        user_name = serializer.validated_data.get('name', "")

        try:
            user = User.objects.get(id=user_id)
            return Response(status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            User.objects.create(id = user_id, name = user_name)
            return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def info(request):
    """
    ユーザー情報の取得
    """
    return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_avatar(request):
    try:
        avatar = AvatarSerialzer(data = request.data)
        if avatar.is_valid():
            old_avatar = request.user.avatar
            user_dir = os.path.join(settings.BASE_DIR, 'static/avatar/{}'.format(request.user.id))
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            if old_avatar:
                old_avatar.delete()
            
            request.user.avatar = avatar.validated_data.get('avatar')
            request.user.save()
            return Response(request.user.avatar.url)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_name(request):
    name = request.data.get('name', "")
    if name.strip() == "":
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        request.user.name = name.strip()
        request.user.save()
        return Response(status=status.HTTP_200_OK)