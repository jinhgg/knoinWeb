from rest_framework.response import Response
from rest_framework.views import APIView

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
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = ProjectFilter
    search_fields = '__all__'

    permission_classes_by_action = {
        'create': [],
        'list': [],
        'retrieve': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated]
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
        # p = request.data
        osList = []
        import os
        cmd = 'ps -ef'
        textlist = os.popen(cmd).readlines()
        for line in textlist:
            osList.append(line)
        return Response({'message':'ok', 'os': osList}, status=status.HTTP_200_OK)


class GenShFileView(APIView):
    """
    run analysis script.
    """
    def post(self, request, format=None):
        params = request.data
        render_file(params)
        osList = []
        import os
        cmd = 'ps -ef'
        textlist = os.popen(cmd).readlines()
        for line in textlist:
            osList.append(line)
        return Response({'message':'ok', 'os': osList}, status=status.HTTP_200_OK)
