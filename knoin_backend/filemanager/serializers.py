from filemanager.models import FileManager
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileManager
        fields = '__all__'
