from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from knoin_backend.utils.permission import IsHimself
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes_by_action = {
        'create': [],
        'list': [AllowAny],
        'retrieve': [IsAuthenticated, IsHimself],
        'update': [IsAuthenticated, IsHimself],
        'partial_update': [IsAuthenticated, IsHimself],
        'destroy': [IsAdminUser]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
