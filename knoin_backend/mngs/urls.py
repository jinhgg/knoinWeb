from django.urls import path
from rest_framework.routers import DefaultRouter

from mngs.views import ProjectViewSet, CollectionViewSet, RunScriptView, GenShFileView, StartAnalysView, UpdateStateView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'collections', CollectionViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('runscript/', RunScriptView.as_view()),
    path('genshfile/', GenShFileView.as_view()),
    path('startanalys/', StartAnalysView.as_view()),
    path('updatestate/', UpdateStateView.as_view()),
]
