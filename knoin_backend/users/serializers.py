from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    token = serializers.CharField(read_only=True)  # 只返回，不校验的字段写这里

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'password', 'token']  # 这里决定了接口文档表单项
        extra_kwargs = {  # 写在这里，不显示声明，返回的错误信息更详细
            'username': {
                'help_text': '用户名，3~50个字符',
                'max_length': 50,
                'min_length': 3,
                'error_messages': {
                    'blank': '用户名不能为空',
                    'required': '用户名不能为空',
                    'max_length': '用户名应在3~50位之间',
                    'min_length': '用户名应在3~50位之间'
                },
                'validators': [UniqueValidator(queryset=User.objects.all(), message='用户名已被注册')]
            },
            'mobile': {
                'help_text': '手机号，11个字符',
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
                'help_text': '密码，3~50个字符',
                'write_only': True,
                'min_length': 3,
                'max_length': 50,
                'error_messages': {
                    'blank': '密码不能为空',
                    'required': '密码不能为空',
                    'min_length': '密码长度不能小于3位',
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

        # 注册后返回token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt
        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成完整的jwt
        user.token = token

        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data=validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return user
