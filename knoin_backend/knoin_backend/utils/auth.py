import jwt
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, jwt_decode_handler
from rest_framework import exceptions

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数,多追加 id,username,mobile"""
    return {
        'success': True,
        'id': user.id,
        'username': user.username,
        'mobile': user.mobile,
        'token': token
    }


class UsernameMobileAuthBackend(ModelBackend):
    """修改Django的认证类,为了实现用户名和手机号两种方式登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取到user
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


# 重写校验header中token的方法，登录token-auth不经过这里
class MyJwtAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            raise exceptions.AuthenticationFailed('token不能为空')

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)
