from django.urls import path
from users.views import RegisterView
from django.conf.urls import url

urlpatterns = [
    # path('users/', ceshi),
    path('users/', RegisterView.as_view()),

]
