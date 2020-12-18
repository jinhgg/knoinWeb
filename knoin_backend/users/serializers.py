from rest_framework import serializers
from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    username = serializers.CharField()
    mobile = serializers.CharField()
    password = serializers.CharField(write_only=True)  # write_only为true表示只校验(反序列化)不返回(序列化)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
