from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """自定义用户模型类"""
    username = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=11, unique=True)
