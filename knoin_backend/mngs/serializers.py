from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings

from mngs.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    # token = serializers.CharField(read_only=True)  # 只返回，不校验的字段写这里

    class Meta:
        model = Project
        fields = '__all__'  # 这里决定了接口文档表单项
