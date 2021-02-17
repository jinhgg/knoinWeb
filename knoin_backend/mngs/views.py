import os

import rest_framework_jwt
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from django.core.files.base import ContentFile, File
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from filemanager.models import FileManager
from knoin_backend.utils.auth import MyJwtAuthentication
from knoin_backend.utils.permission import IsHimself
from knoin_backend.utils.render import render
from knoin_backend.utils.runscript import runscript
from mngs.serializers import ProjectSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from mngs.models import Project, Collection

from rest_framework import filters, status
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters import rest_framework
from mngs.filters import ProjectFilter, CollectionFilter


class ProjectViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Project instances.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # 筛选和排序功能，现在是最简单的筛选和排序，复杂的筛选参考教程：https://zhuanlan.zhihu.com/p/110060840
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ProjectFilter
    permission_classes = []
    # permission_classes_by_action = {
    #     'create': [],
    #     'list': [],
    #     'retrieve': [],
    #     'update': [],
    #     'partial_update': [],
    #     'destroy': []
    # }
    #
    # def get_permissions(self):
    #     try:
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError:
    #         return [permission() for permission in self.permission_classes]


class CollectionViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Collection instances.
    """
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = CollectionFilter
    page_size = 4
    permission_classes_by_action = {
        'create': [],
        'list': [],
        'retrieve': [],
        'update': [],
        'partial_update': [],
        'destroy': []
    }

    # 重写文件删除方法
    def perform_destroy(self, instance):
        Project.objects.filter(collection_id=instance.id).delete()
        instance.delete()

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class RunScriptView(APIView):
    """
    run analysis script.
    """
    # self.dispatch
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


class SaveAnalysView(APIView):
    """
    run analysis script.
    """

    def post(self, request):
        # 1.获取项目对象
        collection_id = request.data.get('collection_id')
        ctrl_path = request.data.get('ctrl_path')
        projects_list = request.data.get('projects_list')
        if not projects_list:
            return Response({'项目不存在'}, status=status.HTTP_400_BAD_REQUEST)
        collection = Collection.objects.get(id=collection_id)
        if not collection:
            return Response({'此项目不存在'}, status=status.HTTP_400_BAD_REQUEST)
        if not os.path.exists(ctrl_path):
            return Response({'对照文件错误'}, status=status.HTTP_400_BAD_REQUEST)
        collection.ctrl_file_path = ctrl_path

        for p in projects_list:
            project = Project.objects.get(id=p.get('id'))
            analys_file_path = p.get('analys_file_path')
            if not os.path.exists(analys_file_path):
                return Response({'样本{}分析文件错误'.format(project.client_name)}, status=status.HTTP_400_BAD_REQUEST)
            project.analys_file_path = analys_file_path
            project.save()

        collection.save()
        return Response({'ok'}, status=status.HTTP_200_OK)


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
        if not collection.ctrl_file_path or not os.path.exists(collection.ctrl_file_path):
            return Response({'对照文件错误'}, status=status.HTTP_400_BAD_REQUEST)
        projects = Project.objects.filter(collection_id=collection_id)
        if not projects:
            return Response({'此项目不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 分析文件路径列表
        client_file_pair_list = []
        for project in projects:
            if not project.analys_file_path or not os.path.exists(project.analys_file_path):
                return Response({'样本{}:分析文件错误'.format(project.client_no)}, status=status.HTTP_400_BAD_REQUEST)
            # analys_file_path = FileManager.objects.get(name=project.analys_file_name).file.path
            client_file_pair_list.append(
                {'client_no': project.client_no, 'analys_file_path': project.analys_file_path}
            )

        # 样本文件路径
        ctrl_file_path = collection.ctrl_file_path

        sys_ini_str = render({}, 'sys.ini').encode(encoding='UTF-8')
        collection.sys_ini.save('sys.ini', ContentFile(sys_ini_str))

        out_dir = '/mnt/sda/platform/result_data/' + collection.name
        control_dir = '/mnt/sda/platform/control_sh'
        sections = 'fastp,classify,classifycal,fasta,classifyg,classifygcal,fastag,res'
        sam_ini_str = render({
            'client_file_pair_list': client_file_pair_list,
            'ctrl_file_path': ctrl_file_path,
            'out_dir': out_dir,
            'sections': sections
        }, 'sam.ini').encode(encoding='UTF-8')
        collection.sam_ini.save('sam.ini', ContentFile(sam_ini_str))

        main_sh_str = render({}, 'main.sh').encode(encoding='UTF-8')
        collection.main_sh.save('main.sh', ContentFile(main_sh_str))

        with open(control_dir + '/{}.sh'.format(collection.name), 'w+') as f:
            f.write('mkdir {out_dir}\n'
                    'mv {main_sh_path} {out_dir}/main.sh\n'
                    'mv {sam_path} {out_dir}/mNGS_config_sam.ini\n'
                    'mv {sys_path} {out_dir}/mNGS_config_sys_bgi.ini\n'
                    'cd {out_dir}\n'
                    'chmod 777 main.sh\n'
                    'main.sh>main.sh.o 2>main.sh.e &'.format(main_sh_path=collection.main_sh.path,
                                                             sys_path=collection.sys_ini.path,
                                                             sam_path=collection.sam_ini.path, out_dir=out_dir))

        cmd = 'bash {}'.format(control_dir + '/{}.sh'.format(collection.name))
        print(cmd)
        runscript(cmd)
        collection.status = '正在分析'
        collection.sections = sections
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
        # collection_dir = os.path.dirname(os.path.dirname(analysing_collection.sys_ini.path))
        collection_dir = '/mnt/sda/platform/result_data/' + analysing_collection.name
        if not os.listdir(collection_dir + '/classifyg'):
            # 没有分析完成的情况
            bp_path = collection_dir + '/' + 'breakpoint'
            print(bp_path)
            if not os.path.exists(bp_path):
                return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)
            with open(bp_path, 'r') as bp:
                sections = bp.read()
                print(sections)

            finishec_sections = ','.join(sections.split('\n'))
            analysing_collection.finished_sections = finishec_sections
            analysing_collection.save()
            return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)

        projects = Project.objects.filter(collection_id=collection_id)
        if not projects:
            return Response({''}, status=status.HTTP_204_NO_CONTENT)

        result_file_list = []
        for project in projects:
            # 1.保存质控图片 LX2004622.Qual_lines.png
            qc_image_path = collection_dir + '/filter/' + project.client_no + '/{}.Qual_lines.png'.format(
                project.client_no)
            if not os.path.exists(qc_image_path):
                return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)
            qc_image = open(qc_image_path, 'rb').read()
            project.qc_image.save('{}_qc_image.png'.format(project.client_no), ContentFile(qc_image))

            # 2.质控结果1
            qc_path = collection_dir + '/classifyg/{}.classify_qc.xls'.format(
                project.client_no)
            if not os.path.exists(qc_path):
                return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)
            qc = open(qc_path)
            project.qc.save('{}_qc.xls'.format(project.client_no), File(qc))

            # 3.质控结果2
            kraken2_qc_path = collection_dir + '/filter/' + project.client_no + '/{}.qc.xls'.format(
                project.client_no)
            if not os.path.exists(kraken2_qc_path):
                return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)
            kraken2_qc = open(kraken2_qc_path)
            project.kraken2_qc.save('{}_qc2.xls'.format(project.client_no), File(kraken2_qc))

            # 4.分析结果 LX2004793.kraken2_abundance_result.anno
            analys_report_path = collection_dir + '/classify/{}.classify_abundance_result.anno.xls'.format(
                project.client_no)
            if not os.path.exists(analys_report_path):
                return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)
            for line in open(analys_report_path, encoding='utf8').readlines():
                with open(collection_dir + '/classify/{}.classify_abundance_result_conv.anno.xls'.format(
                        project.client_no), "a", encoding='utf_8_sig') as f:
                    f.write(line)

            analys_report = open(collection_dir + '/classify/{}.classify_abundance_result_conv.anno.xls'.format(
                project.client_no))
            project.analys_report.save('{}_result.xls'.format(project.client_no), File(analys_report))

            result_file_list.append(project.analys_report.path)

            project.status = '分析完成'
            project.save()

        import zipfile
        zip_file = zipfile.ZipFile(collection_dir + '/results.zip', 'w', zipfile.ZIP_DEFLATED)
        print(result_file_list)
        for i in result_file_list:
            file_name = i.split('/')[-1]
            zip_file.write(i, file_name)  # 这个file是文件名，意思是直接把文件添加到zip没有文件夹层级， f.write(i)这种写法，则会出现上面路径的层级
            # print(zip_file.read())
        zip_file.close()

        # results_zip_file = open(collection_dir)
        analysing_collection.results_zip_path = collection_dir + '/results.zip'
        analysing_collection.status = '分析完成'
        analysing_collection.save()
        return Response({''}, status=status.HTTP_204_NO_CONTENT)


class GenReportView(APIView):
    """
    生成报告
    """

    def post(self, request):
        """
        :param request:
        :return:
        """
        project_id = request.data.get('project_id')
        project = Project.objects.get(id=project_id)
        if not project:
            return Response({''}, status=status.HTTP_400_BAD_REQUEST)

        template_name = request.data.get('template_name')
        if not template_name:
            return Response({''}, status=status.HTTP_400_BAD_REQUEST)

        tpl = DocxTemplate('/home/lijh/knoinWeb/knoin_backend/templates/{}.docx'.format(template_name))

        dataList = request.data.get('dataList')
        if not dataList:
            return Response({''}, status=status.HTTP_400_BAD_REQUEST)

        f_results_list = []
        important_f_results_list = []
        f_results = []
        important_f_results = []

        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        list7 = []
        list8 = []
        list9 = []
        list10 = []
        list11 = []  # RNA病毒
        for i in dataList:
            if i.get('status') == '背景微生物':
                list9.append(i)
            elif i.get('sub_type') == '细菌':
                list1.append(i)
            elif i.get('sub_type') == '真菌':
                list2.append(i)
            elif i.get('sub_type') in 'DNA病毒':
                list3.append(i)
            elif i.get('sub_type') in 'RNA病毒':
                list11.append(i)
            elif i.get('sub_type') in '寄生虫':
                list4.append(i)
            elif i.get('sub_type') in '结核分枝杆菌':
                list5.append(i)
            elif i.get('sub_type') in '非结核分枝杆菌':
                list6.append(i)
            elif i.get('sub_type') in '支原体/衣原体':
                list7.append(i)
            elif i.get('sub_type') in '耐药基因':
                list8.append(i)
            else:
                pass

            if i.get('status') == '关注':
                f_results.append(i.get('species_Cname'))
                f_results_list.append(i)
                desc = i.get('des_C')
                if desc and desc != '-':
                    if '）' in desc:
                        i['des_C'] = desc[desc.index('）') + 1:]
                list10.append(i)
            if i.get('status') == '重点关注':
                important_f_results.append(i.get('species_Cname'))
                important_f_results_list.append(i)
                desc = i.get('des_C')
                if desc and desc != '-':
                    if '）' in desc:
                        i['des_C'] = desc[desc.index('）') + 1:]
                list10.append(i)

            list1_7 = list1 + list7

        if not f_results and not important_f_results:
            fh = '-'
            explain = '无'
        else:
            fh = '+'
            explain = ''
        f_results = '、'.join(f_results)
        important_f_results = '、'.join(important_f_results)
        with open(project.qc.path) as f:
            qc_file = f.read().split('\t')
        with open(project.kraken2_qc.path) as f:
            qc2_file = f.read()
        all_reads = qc_file[3].split('\n')[1]
        non_human = qc_file[4]
        non_human_fre = qc_file[5]
        q20 = qc_file[6].split('\n')[0]
        q30 = qc2_file.split('\t')[-1].strip('\n')
        img = InlineImage(tpl, project.qc_image.path, width=Cm(17.95))
        linchuang = '，'.join({project.diagnosis, project.clinical_manifestations})
        age = project.age + '岁' if '天' not in project.age and '岁' not in project.age and project.age != '-' else project.age
        empty_list = [{'not_found': '未发现'}]
        context = {"name": project.patient_name,
                   "sex": project.gender,
                   "num": project.client_no,
                   "age": age,
                   "linchuang": linchuang,
                   "result": project.detect_result,
                   "important": project.pathogen if project.pathogen else '',
                   "hospital": project.hospital,
                   "Sample_type": project.sample_type,
                   "Department": project.department,
                   "Sampling_date": project.sampling_date,
                   "physician": project.dockor_name,
                   "Test_date": project.collect_date,
                   "report_date": project.report_time,
                   'important_f_results': important_f_results,
                   'f_results': f_results,
                   'important_f_results_list': important_f_results_list,
                   'f_results_list': f_results_list,
                   'list_1': list1 if list1 else empty_list,  # Bacteria
                   'list_2': list2 if list2 else empty_list,  # Fungi
                   'list_3': list3 if list3 else empty_list,  # Viruses
                   'list_4': list4 if list4 else empty_list,  # Parasite
                   'list_5': list5 if list5 else empty_list,
                   'list_6': list6 if list6 else empty_list,
                   'list_7': list7 if list7 else empty_list,
                   'list_8': list8 if list8 else empty_list,
                   'list_9': list9 if list9 else empty_list,
                   'list_10': list10 if list10 else empty_list,
                   'list1_7': list1_7 if list1_7 else empty_list,
                   'all_reads': all_reads,
                   'non_human': non_human,
                   'non_human_fre': non_human_fre,
                   'q20': q20, 'q30': q30, 'img': img, 'explain': explain,
                   'tpl': tpl, 'fh': fh}
        context['tpl'].render(context)
        report_name = '诺微因病原微生物宏基因组测序检测报告-{}_{}.docx'.format(template_name, project.patient_name)
        report_path = '/home/lijh/knoinWeb/knoin_backend/statics/' + report_name
        tpl.save(report_path)
        return Response({'report_link': 'http://192.168.3.19:1080/statics/' + report_name},
                        status=status.HTTP_200_OK)
