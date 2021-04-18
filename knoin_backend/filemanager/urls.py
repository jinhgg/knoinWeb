from django.urls import path

from filemanager.views import FileViewSet, GetFileListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'files', FileViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('filelist/', GetFileListView.as_view()),
]