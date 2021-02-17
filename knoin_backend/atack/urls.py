from django.urls import path
from rest_framework.routers import DefaultRouter

from atack.views import AlbumViewSet, TrackViewSet
from mngs.views import ProjectViewSet, CollectionViewSet, RunScriptView, GenShFileView, StartAnalysView, \
    UpdateStateView, GenReportView, SaveAnalysView

router = DefaultRouter()
router.register(r'tracks', TrackViewSet)
router.register(r'albums', AlbumViewSet)
urlpatterns = router.urls

