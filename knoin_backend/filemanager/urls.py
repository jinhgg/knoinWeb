from filemanager.views import FileViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'file', FileViewSet)
urlpatterns = router.urls
