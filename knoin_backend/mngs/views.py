from mngs.serializers import ProjectSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from mngs.models import Project

from rest_framework import filters
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


# class FilePathList(APIView):
#     """
#     List file path.
#     """
#     def get(self, request, format=None):
#
#         return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)