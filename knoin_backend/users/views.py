from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from users.models import User
from users.serializers import CreateUserSerializer
from rest_framework.response import Response


class RegisterView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer

# class ChecksUsernameView(APIView):
#     """用户名校验"""
#
#     def get(self, request, username):
#         msg = {
#             'code': username
#
#         }
#         count = User.objects.filter(username=username).count()
#         if count:
#
#         # 包装响应数据
#         data = {
#             'username': username,
#             'count': count
#         }
#         # 响应
#         return Response(data)
