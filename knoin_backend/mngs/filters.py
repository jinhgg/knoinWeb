import django_filters
from mngs.models import Project


class ProjectFilter(django_filters.rest_framework.FilterSet):
    """
    Project过滤器
    """

    class Meta:
        model = Project
        fields = '__all__'
