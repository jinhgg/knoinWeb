from django.urls import path
from rest_framework.routers import DefaultRouter

from mngs.views import ProjectViewSet, CollectionViewSet, StartAnalysView, \
    UpdateStateView, GenReportView, TestView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'collections', CollectionViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('startanalys/', StartAnalysView.as_view()),
    path('updatestate/', UpdateStateView.as_view()),
    path('gen-report/', GenReportView.as_view()),
    path('test/', TestView.as_view()),

]
