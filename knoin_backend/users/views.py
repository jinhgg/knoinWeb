from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer



# class RegisterView(CreateAPIView):
#     """用户注册"""
#     serializer_class = UserCreateSerializer


# class UserDetailView(RetrieveAPIView):
#     """用户详细信息"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserListView(ListCreateAPIView):
#     """用户列表信息"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()