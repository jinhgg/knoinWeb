import re
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
        fields = ['id', 'username', 'password', 'password2', 'mobile']

    def validate_mobile(self, value):
        """手机号校验"""
        if not re.match(r'1[3-9]\d{9}$', value):
            print(111)
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            print(222)
            raise serializers.ValidationError('两次密码输入不一致')
        return attrs

    def create(self, validated_data):
        print(333)
        del validated_data['password2']
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

