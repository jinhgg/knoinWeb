import os

from django.core.files.base import ContentFile, File
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from filemanager.models import FileManager
from knoin_backend.utils.render import render
from knoin_backend.utils.runscript import runscript
from mngs.serializers import ProjectSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from mngs.models import Project, Collection

from rest_framework import filters, status
from django_filters import rest_framework
from mngs.filters import ProjectFilter, CollectionFilter


class ProjectViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Project instances.
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


class CollectionViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Collection instances.
    """
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CollectionFilter
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
        collection_id = request.data.get('collection_id')
        collection = Collection.objects.get(id=collection_id)
        if not collection:
            return Response({'此项目不存在'}, status=status.HTTP_400_BAD_REQUEST)
        if not collection.ctrl_file_path:
            return Response({'缺少参考文件'}, status=status.HTTP_400_BAD_REQUEST)

        projects = Project.objects.filter(collection_id=collection_id)
        if not projects:
            return Response({'此项目不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 分析文件路径列表
        client_file_pair_list = []
        for project in projects:
            if not project.analys_file_path:
                return Response({'缺少分析文件'}, status=status.HTTP_400_BAD_REQUEST)
            # analys_file_path = FileManager.objects.get(name=project.analys_file_name).file.path
            client_file_pair_list.append(
                {'client_no': project.client_no, 'analys_file_path': project.analys_file_path}
            )

        # 样本文件路径
        ctrl_file_path = collection.ctrl_file_path

        sys_ini_str = render({}, 'sys.ini').encode(encoding='UTF-8')
        collection.sys_ini.save('sys.ini', ContentFile(sys_ini_str))

        sam_ini_str = render({
            'client_file_pair_list': client_file_pair_list,
            'ctrl_file_path': ctrl_file_path,
            'out_dir': os.path.dirname(os.path.dirname(collection.sys_ini.path)),
        }, 'sam.ini').encode(encoding='UTF-8')

        collection.sam_ini.save('sam.ini', ContentFile(sam_ini_str))

        main_sh_str = render({'sam_ini_path': collection.sam_ini.path, 'sys_ini_path': collection.sys_ini.path},
                             'main.sh').encode(encoding='UTF-8')
        collection.main_sh.save('main.sh', ContentFile(main_sh_str))

        with open(os.path.dirname(os.path.dirname(collection.sys_ini.path)) + '/control.sh', 'w+') as f:
            f.write(
                'cd {}\nchmod 777 main.sh\nmain.sh>main.sh.o 2>main.sh.e &'.format(
                    os.path.dirname(collection.sys_ini.path)))

        cmd = 'bash {}'.format(os.path.dirname(os.path.dirname(collection.sys_ini.path)) + '/control.sh')
        print(cmd)
        runscript(cmd)
        collection.status = '正在分析'
        collection.save()

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
        collection_id = request.data.get('collection_id')
        analysing_collection = Collection.objects.get(id=collection_id)
        if not analysing_collection:
            return Response({''}, status=status.HTTP_204_NO_CONTENT)

        # collection_dir /20210119
        collection_dir = os.path.dirname(os.path.dirname(analysing_collection.sys_ini.path))
        if not os.listdir(collection_dir + '/classify'):
            return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)

        projects = Project.objects.filter(collection_id=collection_id)
        if not projects:
            return Response({''}, status=status.HTTP_204_NO_CONTENT)

        for project in projects:
            # 1.保存质控图片 LX2004622.Qual_lines.png
            qc_image_path = collection_dir + '/filter/' + project.client_no + '/{}.Qual_lines.png'.format(
                project.client_no)
            qc_image = open(qc_image_path, 'rb').read()
            project.qc_image.save('qc_image.png', ContentFile(qc_image))

            # 2.质控结果1
            qc_path = collection_dir + '/classify/{}.classify_qc.xls'.format(
                project.client_no)
            qc = open(qc_path)
            project.qc.save('qc.xls', File(qc))

            # 3.质控结果2
            kraken2_qc_path = collection_dir + '/filter/' + project.client_no + '/{}.qc.xls'.format(
                project.client_no)
            kraken2_qc = open(kraken2_qc_path)
            project.kraken2_qc.save('qc2.xls', File(kraken2_qc))

            # 4.分析结果 LX2004793.kraken2_abundance_result.anno
            analys_report_path = collection_dir + '/classify/{}.classify_abundance_result.anno.xls'.format(
                project.client_no)
            analys_report = open(analys_report_path)
            project.analys_report.save('analys_report.xls', File(analys_report))

            project.status = '分析完成'
            project.save()

        analysing_collection.status = '分析完成'
        analysing_collection.save()
        return Response({''}, status=status.HTTP_204_NO_CONTENT)

        # with open(os.path.dirname(os.path.dirname(project.sys_ini.path))+'/test.sh') as f:
        #     f.write(
        #         'cd {}\nmain.sh>main.sh.o 2>main.sh.e &'.format(os.path.dirname(os.path.dirname(project.sys_ini.path))))
        #
        # cmd = 'sh {path}/'.format(path=project.main_sh.path)
