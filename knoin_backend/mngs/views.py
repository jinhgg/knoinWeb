import os
import json
from django.core.cache import cache
from django.shortcuts import get_object_or_404, get_list_or_404
from docxtpl import DocxTemplate
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from knoin_backend.const import Const
from knoin_backend.utils.exceptions import logger

from knoin_backend.utils.render import render
from knoin_backend.utils.runscript import runscript
from mngs.parse_utils import parse_test_date, parse_age, parse_diagnosis, parse_qc_result, \
    parse_detect_data, parse_img, parse_date, parse_pathogen
from mngs.serializers import ProjectSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
from mngs.models import Project, Collection
from rest_framework import filters, status
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


class CollectionViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Collection instances.
    """
    serializer_class = CollectionSerializer
    queryset = Collection.objects.order_by('-id').all()
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
        return [permission() for permission in self.permission_classes_by_action[self.action]]


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
        collection = get_object_or_404(Collection, id=collection_id)
        ctrl_file_path = collection.ctrl_file_path
        if not ctrl_file_path:
            return Response({'缺少对照文件'}, status=status.HTTP_400_BAD_REQUEST)
        if not os.path.isfile(ctrl_file_path):
            return Response({'对照文件路径错误'}, status=status.HTTP_400_BAD_REQUEST)

        projects = get_list_or_404(Project, collection_id=collection_id)

        # 分析文件路径列表
        client_file_pair_list = []
        for project in projects:
            if not project.analys_file_path or not os.path.isfile(project.analys_file_path):
                return Response({'样本{}:分析文件错误'.format(project.client_no)}, status=status.HTTP_400_BAD_REQUEST)
            client_file_pair_list.append(
                {'client_no': project.client_no, 'analys_file_path': project.analys_file_path}
            )

        # 样本文件路径
        ctrl_file_path = collection.ctrl_file_path

        sys_ini_str = render({}, 'sys.ini').encode(encoding='UTF-8')
        collection.sys_ini.save('sys.ini', ContentFile(sys_ini_str))

        out_dir = '/mnt/sda/platform/result_data/' + collection.name
        control_dir = '/mnt/sda/platform/control_sh'
        sections = 'filter,human,classify,classifycal,fasta,res,autoscreen'
        sam_ini_str = render({
            'client_file_pair_list': client_file_pair_list,
            'ctrl_file_path': ctrl_file_path,
            'out_dir': out_dir,
            'sections': sections
        }, 'sam.ini').encode(encoding='UTF-8')
        collection.sam_ini.save('sam.ini', ContentFile(sam_ini_str))

        main_sh_str = render({'collection_name': collection.name}, 'main.sh').encode(encoding='UTF-8')
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
        collection_name = request.data.get('collection_name')
        if collection_id:
            analysing_collection = get_object_or_404(Collection, id=collection_id)
        else:
            analysing_collection = get_object_or_404(Collection, name=collection_name)
        # collection_dir /20210119
        # collection_dir = os.path.dirname(os.path.dirname(analysing_collection.sys_ini.path))
        collection_dir = '/mnt/sda/platform/result_data/{}'.format(analysing_collection.name)
        collection_result_dir = '/mnt/sda/platform/result_data/{}/result'.format(analysing_collection.name)

        if not os.path.exists(collection_dir):
            return Response({'项目还未开始分析'}, status=status.HTTP_204_NO_CONTENT)
        bp_path = collection_dir + '/breakpoint'
        if os.path.exists(bp_path):
            with open(bp_path, 'r') as bp:
                sections = bp.read()
        else:
            sections = ''

        if not os.listdir(collection_result_dir + '/classify'):
            # 没有分析完成的情况
            finished_sections = ','.join(sections.split('\n'))
            analysing_collection.finished_sections = finished_sections
            analysing_collection.save()
            return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)

        projects = get_list_or_404(Project, collection_id=analysing_collection.id)
        result_file_list = []
        for project in projects:
            # 分析结果 LX2004793.kraken2_abundance_result.anno
            analys_report_path = collection_result_dir + '/classify/{}.classify_abundance_result.anno.xls'.format(
                project.client_no)
            analys_report_conv_path = collection_result_dir + '/classify/{}.classify_abundance_result_conv.anno.xls'.format(
                project.client_no)
            if not os.path.exists(analys_report_path):
                return Response({'正在分析'}, status=status.HTTP_204_NO_CONTENT)

            with open(analys_report_path, 'r', encoding='utf8') as f:
                analys_report_filelines = f.readlines()
            with open(analys_report_conv_path, 'w', encoding='utf_8_sig') as f:
                f.writelines(analys_report_filelines)

            # 保存质控图片 LX2004622.Qual_lines.png
            qc_image_path = collection_result_dir + '/filter/' + project.client_no + '/{}.Qual_lines.png'.format(
                project.client_no)
            if os.path.exists(qc_image_path):
                project.qc_image_path = qc_image_path

            # 质控结果1
            # qc_path = collection_result_dir + '/classifyg/{}.classify_qc.xls'.format(
            #     project.client_no)
            qc_path = collection_result_dir + '/classify/{}.classify_qc.xls'.format(
                project.client_no)
            if os.path.exists(qc_path):
                project.qc_path = qc_path

            # 3.质控结果2
            kraken2_qc_path = collection_result_dir + '/filter/' + project.client_no + '/{}.qc.xls'.format(
                project.client_no)
            if os.path.exists(kraken2_qc_path):
                project.kraken2_qc_path = kraken2_qc_path

            project.analys_report_path = analys_report_conv_path
            result_file_list.append(analys_report_conv_path)
            project.status = '分析完成'
            project.save()

        import zipfile
        zip_file = zipfile.ZipFile(collection_result_dir + '/results.zip', 'w', zipfile.ZIP_DEFLATED)
        for i in result_file_list:
            file_name = i.split('/')[-1]
            zip_file.write(i, file_name)  # 这个file是文件名，意思是直接把文件添加到zip没有文件夹层级， f.write(i)这种写法，则会出现上面路径的层级
        zip_file.close()

        # results_zip_file = open(collection_dir)
        analysing_collection.results_zip_path = collection_result_dir + '/results.zip'
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
        mode = request.data.get('mode')
        if mode == 'auto':
            project_id = request.data.get('project_id')
            if not project_id:
                project_client_no = request.data.get('project_client_no')
                project = get_object_or_404(Project, client_no=project_client_no)
            else:
                project = get_object_or_404(Project, id=project_id)
            report_format = project.report_format
            detect_type = project.detect_type

            template_name = request.data.get('template_name')
            if not template_name:
                if not detect_type:
                    report_type = 'DNA'
                elif 'RNA' in detect_type:
                    report_type = 'DNA+RNA'
                else:
                    report_type = 'DNA'

                if 'pdf' in report_format:
                    template_name = report_type
                elif '洛兮' in report_format:
                    template_name = '洛兮'
                elif '白版' in report_format:
                    template_name = '白版'
                elif '云量' in report_format:
                    template_name = '广州_' + report_type
                elif '盖章' in report_format:
                    template_name = '福建_' + report_type
                else:
                    return Response({'报告版式名称不正确'}, status=status.HTTP_400_BAD_REQUEST)

            collection = project.collection
            auto_gen_json_result_path = Const.AUTO_GEN_JSON_RESULT_PATH.format(collection_name=collection.name,
                                                                               client_no=project.client_no)
            if not os.path.exists(auto_gen_json_result_path):
                return Response({'数据为空'}, status=status.HTTP_400_BAD_REQUEST)
            with open(auto_gen_json_result_path, 'r') as f:
                data_list_json = f.read()
            data_list = json.loads(data_list_json)

        else:
            project_id = request.data.get('project_id')
            logger.info(project_id)
            project = get_object_or_404(Project, id=project_id)
            collection = project.collection
            data_list = request.data.get('dataList')
            template_name = request.data.get('template_name')
            if not template_name:
                return Response({'请选择模板'}, status=status.HTTP_400_BAD_REQUEST)

        template_path = Const.TEMPLATE_PATH.format(template_name=template_name)
        tpl = DocxTemplate(template_path)
        # 直接通过project获取的信息
        name = project.patient_name
        sex = project.gender
        num = project.client_no
        sample_volume = project.sample_size
        result = project.detect_result
        hospital = project.hospital
        sample_type = project.sample_type
        department = project.department
        physician = project.dockor_name
        report_date = project.report_time

        pathogen = parse_pathogen(project.pathogen)
        test_date = parse_test_date(project.report_time)
        convey_date = parse_date(project.convey_date)
        sampling_date = parse_date(project.sampling_date)
        age = parse_age(project.age)
        age_luo = age[:-1]
        diagnosis = parse_diagnosis(project.diagnosis)
        qc_result = parse_qc_result(project.qc_path, project.kraken2_qc_path)
        img = parse_img(tpl, project.qc_image_path)

        detect_data = parse_detect_data(data_list)

        tpl.render(locals())

        if '白版' in template_name:
            report_name = Const.REPORT_NAME_1.format(patient_name=project.patient_name,
                                                     sample_type=project.sample_type)
        elif template_name == 'DNA' or template_name == 'DNA+RNA':
            report_name = Const.REPORT_NAME_2.format(detect_type='mNGS_' + template_name.split('_')[-1],
                                                     patient_name=project.patient_name,
                                                     sample_type=project.sample_type)
        elif '洛兮' in template_name:
            report_name = Const.REPORT_NAME_3.format(patient_name=project.patient_name,
                                                     sample_type=project.sample_type)
        elif template_name == '广州_DNA' or template_name == '广州_DNA+RNA':
            hospital = Const.HOSPITAL_MAP.get(project.hospital, project.hospital)
            report_name = Const.REPORT_NAME_4.format(hospital=hospital,
                                                     detect_type=template_name.split('_')[-1],
                                                     patient_name=project.patient_name,
                                                     sample_type=project.sample_type)
        else:
            report_name = Const.REPORT_NAME_3.format(detect_type=template_name.split('_')[-1],
                                                     patient_name=project.patient_name,
                                                     sample_type=project.sample_type)

        if collection.status == '待分析' or mode == 'manual':
            report_path = Const.STATIC_PATH + report_name
            report_link = Const.STATIC_URL + report_name
        else:
            report_path = Const.REPORT_PATH.format(collection_name=collection.name, report_name=report_name)
            report_link = Const.REPORT_URL.format(collection_name=collection.name, report_name=report_name)
        tpl.save(report_path)
        return Response({'report_link': report_link}, status=status.HTTP_200_OK)


class TestView(APIView):
    """针对所有用户缓存"""

    def get(self, request):
        timestamp = cache.get('timestamp')
        if not timestamp:
            import time
            timestamp = time.time()
            cache.set('timestamp', timestamp, 30)
        return Response({'timestamp': timestamp}, status=status.HTTP_200_OK)


"""
这种方式缓存,会针对不同用户缓存不同内容,
根据header里的cookie, Accept-Encoding, Accept-Language...来判断是不是同一用户
很难做到把上面字段都统一
@method_decorator(csrf_exempt, name='dispatch')
class TestView(APIView):
    @method_decorator(cache_page(30))
    def get(self, request):
        import time
        timestamp = time.time()
        return Response({'timestamp': timestamp}, status=status.HTTP_200_OK)

"""
