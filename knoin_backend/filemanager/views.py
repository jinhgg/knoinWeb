import os
from rest_framework import viewsets, status
from filemanager.models import FileManager
from filemanager.serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class FileViewSet(viewsets.ModelViewSet):
    queryset = FileManager.objects.all()
    serializer_class = FileSerializer

    # 重写文件删除方法，将数据库记录和文件都删除（否则只删数据库记录文件不删）
    def perform_destroy(self, instance):
        instance.file.delete()  # 文件也删了
        instance.delete()  # 删除记录


class GetFileListView(APIView):
    """获取服务器上指定目录的文件列表"""

    def post(self, request):
        dir = request.data.get('dir')
        if not dir:
            return Response({'缺少目录参数'}, status=status.HTTP_400_BAD_REQUEST)
        if not os.path.exists(dir):
            return Response({'目录不存在'}, status=status.HTTP_400_BAD_REQUEST)

        file_list = os.listdir(dir)
        file_list.sort(reverse=True)
        # file_list = [{'name': i, 'other': ''} for i in os.listdir(dir)]
        """
        file_list = [{'name': i, 'other': ''} for i in os.listdir(dir)]

        """

        return Response({'file_list': file_list}, status=status.HTTP_200_OK)
