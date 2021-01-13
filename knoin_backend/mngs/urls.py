from django.urls import path
from rest_framework.routers import DefaultRouter

from mngs.views import ProjectViewSet, RunScriptView, GenShFileView, StartAnalysView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('runscript/', RunScriptView.as_view()),
    path('genshfile/', GenShFileView.as_view()),
    path('startanalys/', StartAnalysView.as_view()),
]
