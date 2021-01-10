from django.urls import path
from rest_framework.routers import DefaultRouter


from mngs.views import ProjectViewSet, RunScriptView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('runscript/', RunScriptView.as_view())
]


