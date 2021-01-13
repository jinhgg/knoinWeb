from rest_framework import serializers

from mngs.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    # token = serializers.CharField(read_only=True)  # 只返回，不校验的字段写这里

    class Meta:
        model = Project
        fields = '__all__'  # 这里决定了接口文档表单项
        # exclude = ['analys_result']
