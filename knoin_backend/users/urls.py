from django.urls import path
from users.views import UserView,ceshi
from django.conf.urls import url

urlpatterns = [
    # path('users/', ceshi),
    path('users/', UserView.as_view()),

]
