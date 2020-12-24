from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    # todo：1.修改密码没有加密保存，需要重新序列化update方法
    serializer_class = UserSerializer
    queryset = User.objects.all()
