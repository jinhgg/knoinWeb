import os
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView

from filemanager.models import File
from knoin_backend.utils.render import render
from knoin_backend.utils.runscript import runscript
from mngs.serializers import ProjectSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from mngs.models import Project

from rest_framework import filters, status
from django_filters import rest_framework
from mngs.filters import ProjectFilter


class ProjectViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ProjectFilter
    search_fields = '__all__'

    permission_classes_by_action = {
        'create': [],
        'list': [],
        'retrieve': [],
        'update': [],
        'partial_update': [],
        'destroy': []
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class RunScriptView(APIView):
    """
    run analysis script.
    """

    def post(self, request, format=None):
        cmd = request.data.get('cmd')
        if not cmd:
            return Response({'empty cmd'}, status=status.HTTP_204_NO_CONTENT)
        output = runscript(cmd)
        return Response({'message': 'ok', 'output': output}, status=status.HTTP_200_OK)


class GenShFileView(APIView):
    """
    run analysis script.
    """

    def post(self, request, format=None):
        params = request.data.get('params')
        if not params or not isinstance(params, dict):
            return Response({'params error'}, status=status.HTTP_400_BAD_REQUEST)

        # 1.根据模板生成文件内容
        file_str = render(params)
        # 2.写入到临时文件
        with open('temp.sh', 'w') as f:
            f.write(file_str)
        # 3.把文件复制到mngs目录
        cmd = 'cat temp.sh > /home/lijh/mNGS/main.sh'.format(file_str)
        output = runscript(cmd)
        # 4.执行main.sh
        cmd = 'sh /home/lijh/mNGS/main.sh>/home/lijh/mNGS/main.sh.o 2>/home/lijh/mNGS/main.sh.e &'
        output = runscript(cmd)
        return Response({'message': 'ok', 'os': output}, status=status.HTTP_200_OK)


class StartAnalysView(APIView):
    """
    run analysis script.
    """

    def post(self, request, format=None):
        """
        1.获取项目对象
        2.获取其文件存放目录
        3.在其对应的目录生成main.sh sam.ini sys.ini
        4.运行main.sh, 判断返回值是否正确运行

        :param request: 1.project_id
        :param format:
        :return:
        """
        # 1.获取项目对象
        project_id = request.data.get('project_id')
        project = Project.objects.get(id=project_id)
        if not project:
            return Response({'此项目不存在'}, status=status.HTTP_400_BAD_REQUEST)

        if not project.analys_file_name or not project.sample_file_name:
            return Response({'缺少分析文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 分析文件路径
        analys_file_path = File.objects.get(name=project.analys_file_name).file.path
        # 样本文件路径
        sample_file_path = File.objects.get(name=project.sample_file_name).file.path

        sys_ini_str = render({}, 'sys_ini').encode(encoding='UTF-8')
        project.sys_ini.save('sys.ini', ContentFile(sys_ini_str))
        a = os.path.dirname(project.sys_ini.path)

        sam_ini_str = render({
            'analys_file_path_list': [analys_file_path],
            'sample_file_path': sample_file_path,
            'out_dir': os.path.dirname(os.path.dirname(project.sys_ini.path)),
            'client_no': project.client_no
        }, 'sam_ini').encode(encoding='UTF-8')

        project.sam_ini.save('sam.ini', ContentFile(sam_ini_str))

        main_sh_str = render({'sam_ini_path': project.sam_ini.path, 'sys_ini_path': project.sys_ini.path},
                             'main_sh').encode(encoding='UTF-8')
        project.main_sh.save('main.sh', ContentFile(main_sh_str))

        cmd = 'sh {path}>{path}.o 2>{path}.e &'.format(path=project.main_sh.path)
        output = runscript(cmd)

        return Response({output}, status=status.HTTP_400_BAD_REQUEST)
