from django.db import models


class Project(models.Model):
    """自定义mngs检测项目模型类"""

    status = models.CharField(help_text='状态', max_length=150, blank=True, null=True)  # 新创建 待分析 分析中 已完成
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
    collect_date = models.CharField(help_text='收样日期', max_length=150, blank=True, null=True)
    report_time = models.CharField(help_text='报告日期', max_length=150, blank=True, null=True)
    bio_info = models.CharField(help_text='生物信息补充', max_length=150, blank=True, null=True)
    detect_status = models.CharField(help_text='项目状态', max_length=150, blank=True, null=True)
    sample_size = models.CharField(help_text='样本量', max_length=150, blank=True, null=True)
    analys_file_path = models.CharField(help_text='分析文件目录', max_length=150, blank=True, null=True)
    sample_file_path = models.CharField(help_text='样本文件目录', max_length=150, blank=True, null=True)
