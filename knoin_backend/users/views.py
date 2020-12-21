from rest_framework.generics import CreateAPIView
from users.models import User
from users.serializers import CreateUserSerializer
from rest_framework.response import Response


class UserView(CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = CreateUserSerializer

def ceshi(request):
    if request.method == 'POST':
        print(123)

        return Response({'message': 'ok'})