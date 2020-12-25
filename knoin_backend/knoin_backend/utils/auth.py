import re
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数,多追加 id,username,mobile"""
    return {
        'id': user.id,
        'username': user.username,
        'mobile': user.mobile,
        'token': token
    }


class UsernameMobileAuthBackend(ModelBackend):
    """修改Django的认证类,为了实现多账号登录"""

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
