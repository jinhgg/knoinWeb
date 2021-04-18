from django.urls import path
from rest_framework.routers import DefaultRouter

from atack.views import AlbumViewSet, TrackViewSet

router = DefaultRouter()
router.register(r'tracks', TrackViewSet)
router.register(r'albums', AlbumViewSet)
urlpatterns = router.urls

