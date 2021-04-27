from django.db import models


def upload_to_result(instance, filename):
    collection_name = Collection.objects.get(id=instance.collection_id).name
    return '/'.join(['analys_data', collection_name, instance.client_no, 'result', filename])


def upload_to_config(instance, filename):
    return '/'.join(['analys_data', instance.name, 'config', filename])


class Collection(models.Model):
    """项目批次"""
    name = models.CharField(help_text='项目批次', max_length=150, blank=True, null=True)
    sections = models.CharField(help_text='所有模块', max_length=150, blank=True, null=True)
    finished_sections = models.CharField(help_text='已经分析完的模块', max_length=150, default='init', blank=True, null=True)
    status = models.CharField(help_text='状态', max_length=150, blank=True, null=True, default='待分析')  # 待分析 分析中 已完成
    ctrl_file_path = models.CharField(help_text='参考文件绝对路径', max_length=150, blank=True, null=True)
    main_sh = models.FileField(help_text='运行脚本', upload_to=upload_to_config, blank=True, null=True)
    sam_ini = models.FileField(help_text='sam.ini', upload_to=upload_to_config, blank=True, null=True)
    sys_ini = models.FileField(help_text='sys.ini', upload_to=upload_to_config, blank=True, null=True)
    results_zip_path = models.CharField(help_text='分析结果zip文件路径',max_length=500, blank=True, null=True)
    dialogVisible = models.BooleanField(help_text='前端使用字段', default=False, blank=True, null=True)
    user_id = models.CharField(help_text='创建者', max_length=150, blank=True, null=True)



class Project(models.Model):
    """自定义mngs检测项目模型类"""

    collection = models.ForeignKey(Collection, related_name='projects', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(help_text='状态', max_length=150, blank=True, null=True, default='待分析')  # 待分析 分析中 已完成
    client_name = models.CharField(help_text='客户/代理/销售名称', max_length=150, blank=True, null=True)
    client_no = models.CharField(help_text='客户编号', max_length=150, blank=True, null=True)
    knoin_no = models.CharField(help_text='诺因编号', max_length=150, blank=True, null=True)
    sample_type = models.CharField(help_text='样本类型', max_length=150, blank=True, null=True)
    detect_type = models.CharField(help_text='送检项目', max_length=150, blank=True, null=True)
    patient_name = models.CharField(help_text='患者姓名', max_length=150, blank=True, null=True)
    gender = models.CharField(help_text='性别', max_length=150, blank=True, null=True)
    age = models.CharField(help_text='年龄', max_length=150, blank=True, null=True)
    hospital = models.CharField(help_text='医院', max_length=150, blank=True, null=True)
    department = models.CharField(help_text='科室', max_length=150, blank=True, null=True)
    dockor_name = models.CharField(help_text='医生', max_length=150, blank=True, null=True)
    report_format = models.CharField(help_text='报告版式', max_length=150, blank=True, null=True)
    sampling_date = models.CharField(help_text='采样日期', max_length=150, blank=True, null=True)
    diagnosis = models.CharField(help_text='临床诊断', max_length=150, blank=True, null=True)
    pathogen = models.CharField(help_text='关注病原', max_length=150, blank=True, null=True)
    WBC = models.CharField(help_text='WBC', max_length=150, blank=True, null=True)
    CRP = models.CharField(help_text='CRP', max_length=150, blank=True, null=True)
    lymphocytes = models.CharField(help_text='淋巴细胞', max_length=150, blank=True, null=True)
    PCT = models.CharField(help_text='PCT', max_length=150, blank=True, null=True)
    neutr_granule = models.CharField(help_text='中性粒细胞', max_length=150, blank=True, null=True)
    detect_result = models.CharField(help_text='培养鉴定结果', max_length=150, blank=True, null=True)
    clinical_manifestations = models.CharField(help_text='临床表现', max_length=150, blank=True, null=True)
    medication = models.CharField(help_text='用药情况', max_length=150, blank=True, null=True)
    convey_date = models.CharField(help_text='送样日期', max_length=150, blank=True, null=True)
    collect_date = models.CharField(help_text='收样日期', max_length=150, blank=True, null=True)
    report_time = models.CharField(help_text='报告日期', max_length=150, blank=True, null=True)
    bio_info = models.CharField(help_text='生物信息补充', max_length=1500, blank=True, null=True)
    detect_status = models.CharField(help_text='项目状态', max_length=150, blank=True, null=True)
    sample_size = models.CharField(help_text='样本量', max_length=150, blank=True, null=True)
    analys_file_path = models.CharField(help_text='分析文件绝对路径', max_length=150, blank=True, null=True)
    analys_report_path = models.CharField(help_text='分析结果报告', max_length=500, blank=True, null=True)
    qc_path = models.CharField(help_text='质控结果1', max_length=500, blank=True, null=True)
    kraken2_qc_path = models.CharField(help_text='质控结果2', max_length=500, blank=True, null=True)
    qc_image_path = models.CharField(help_text='质控图片', max_length=500, blank=True, null=True)
    dialogVisible = models.BooleanField(help_text='前端使用字段', default=False, blank=True, null=True)
