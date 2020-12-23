from rest_framework.exceptions import _get_error_details
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from users.models import User
from users.serializers import CreateUserSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer
