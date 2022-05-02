from rest_framework import authentication
from rest_framework import exceptions
from .models import Token


class UserIDAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return None
        try:
            token = Token.objects.get(token=token)
            user = token.user
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('トークンが存在しません')
        except BaseException:
            raise exceptions.AuthenticationFailed('ユーザーが存在しません')

        return (user, token)
