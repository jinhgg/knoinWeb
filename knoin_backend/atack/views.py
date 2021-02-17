from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from atack.models import Album, Track
from atack.serializers import AlbumSerializer, TrackSerializer


class TrackViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Project instances.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class AlbumViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Project instances.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
