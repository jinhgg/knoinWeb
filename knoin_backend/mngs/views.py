import os
from base64 import b64encode
from io import BytesIO

from django.core.files.base import ContentFile, File
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from filemanager.models import FileManager
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
        analys_file_path = FileManager.objects.get(name=project.analys_file_name).file.path
        # 样本文件路径
        sample_file_path = FileManager.objects.get(name=project.sample_file_name).file.path

        sys_ini_str = render({}, 'sys_ini').encode(encoding='UTF-8')
        project.sys_ini.save('sys.ini', ContentFile(sys_ini_str))

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
        print(cmd)
        output = runscript(cmd)
        print(output)
        project.status = '正在分析'
        project.save()

        return Response({'已经开始分析'}, status=status.HTTP_200_OK)


class UpdateStateView(APIView):
    """
    获取分析进度
    """

    def post(self, request):
        """
        :param request:
        :return:
        """
        # project_id = request.data.get('project_id')
        analysing_projects = Project.objects.filter(status='正在分析')
        if not analysing_projects:
            return Response({''}, status=status.HTTP_204_NO_CONTENT)

        for project in analysing_projects:
            # 判断project是否分析完成
            if os.listdir(os.path.dirname(os.path.dirname(project.sys_ini.path)) + '/kraken') and \
                    os.listdir(os.path.dirname(os.path.dirname(project.sys_ini.path)) + '/filter'):
                # 1.保存质控图片 LX2004622.Qual_lines.png
                qc_image_path = os.path.dirname(os.path.dirname(
                    project.sys_ini.path)) + '/filter/' + project.client_no + '/{}.Qual_lines.png'.format(
                    project.client_no)
                print(11111)
                qc_image = open(qc_image_path,'rb').read()
                print(22222)
                project.qc_image.save('qc_image.png', ContentFile(qc_image))

                # 2.质控结果1
                qc_path = os.path.dirname(os.path.dirname(
                    project.sys_ini.path)) + '/kraken/{}.kraken2_qc.xls'.format(
                    project.client_no)
                qc = open(qc_path)
                project.qc.save('qc.xls', File(qc))

                # 3.质控结果2
                kraken2_qc_path = os.path.dirname(os.path.dirname(
                    project.sys_ini.path)) + '/filter/' + project.client_no + '/{}.qc.xls'.format(
                    project.client_no)
                kraken2_qc = open(kraken2_qc_path)
                project.qc.save('qc2.xls', File(kraken2_qc))

                # 4.分析结果 LX2004793.kraken2_abundance_result.anno
                analys_report_path = os.path.dirname(os.path.dirname(
                    project.sys_ini.path)) + '/kraken/{}.kraken2_abundance_result.anno.xls'.format(
                    project.client_no)
                analys_report = open(analys_report_path)
                project.qc.save('analys_report.xls', File(analys_report))

                project.status = '分析完成'
                project.save()

        # done_projects = Project.objects.filter(status='分析完成')
        # analysing_projects = Project.objects.filter(status='正在分析')
        # done_serializer = ProjectSerializer(done_projects, many=True)
        # analysing_serializer = ProjectSerializer(analysing_projects, many=True)
        return Response({''}, status=status.HTTP_204_NO_CONTENT)
