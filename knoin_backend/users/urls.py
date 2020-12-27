from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('token-auth/', obtain_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('token-refresh/', refresh_jwt_token)
]


