from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='站点页面标题')),
    path('', include('users.urls')),
    path('mngs/', include('mngs.urls')),
    path('', include('filemanager.urls')),
    path('atack/', include('atack.urls'))
]
