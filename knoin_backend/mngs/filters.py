import django_filters
from mngs.models import Project, Collection


class ProjectFilter(django_filters.rest_framework.FilterSet):
    """
    Project过滤器
    """

    class Meta:
        model = Project
        exclude = ['analys_report', 'kraken2_qc', 'qc', 'qc_image']


class CollectionFilter(django_filters.rest_framework.FilterSet):
    """
    Collection过滤器
    """

    class Meta:
        model = Collection
        exclude = ['main_sh', 'sam_ini', 'sys_ini', 'results_zip_file']
