from django.db import models


class FileManager(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='upload', null=True, blank=True)
