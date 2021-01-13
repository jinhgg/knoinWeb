import django_filters
from mngs.models import Project


class ProjectFilter(django_filters.rest_framework.FilterSet):
    """
    Project过滤器
    """

    class Meta:
        model = Project
        exclude = ['analys_report', 'kraken2_qc', 'qc', 'qc_image', 'main_sh', 'sam_ini', 'sys_ini']
