from rest_framework import viewsets
from filemanager.models import File
from filemanager.serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    # 重写文件删除方法，将数据库记录和文件都删除（否则只删数据库记录文件不删）
    def perform_destroy(self, instance):
        instance.file.delete()  # 文件也删了
        instance.delete()  # 删除记录
