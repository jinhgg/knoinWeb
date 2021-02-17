import django_filters
from mngs.models import Project, Collection


class ProjectFilter(django_filters.rest_framework.FilterSet):
    """
    Project过滤器
    """

    class Meta:
        model = Project
        fields = ['status', 'client_name']  # 定义哪些字段可以筛选
        # exclude = ['analys_report', 'kraken2_qc', 'qc', 'qc_image']


class CollectionFilter(django_filters.rest_framework.FilterSet):
    """
    Collection过滤器
    """

    class Meta:
        model = Collection
        fields = ['status']  # 定义哪些字段可以筛选

        # exclude = ['main_sh', 'sam_ini', 'sys_ini', 'results_zip_file']
