from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'password']  # 这里决定了接口文档表单项
        extra_kwargs = {
            'username': {
                'max_length': 150,
                'min_length': 3,
                'error_messages': {
                    'blank': '用户名不能为空',
                    'required': '用户名不能为空',
                    'max_length': '用户名应在3~150位之间',
                    'min_length': '用户名应在3~150位之间'
                },
                'validators': [UniqueValidator(queryset=User.objects.all(), message='用户名已被注册')]
            },
            'mobile': {
                'max_length': 11,
                'min_length': 11,
                'error_messages': {
                    'blank': '手机号不能为空',
                    'required': '手机号不能为空',
                    'min_length': '手机号格式不正确',
                    'max_length': '手机号格式不正确'
                },
                'validators': [UniqueValidator(queryset=User.objects.all(), message='手机号已被注册')]
            },
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 50,
                'error_messages': {
                    'blank': '密码不能为空',
                    'required': '密码不能为空',
                    'min_length': '密码长度不能小于6位',
                    'max_length': '密码长度不能大于50位'
                }
            }
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data=validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return user
