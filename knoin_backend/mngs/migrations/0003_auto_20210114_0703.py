# Generated by Django 3.1.4 on 2021-01-14 07:03

from django.db import migrations, models
import mngs.models


class Migration(migrations.Migration):

    dependencies = [
        ('mngs', '0002_auto_20210113_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='qc_image',
            field=models.ImageField(blank=True, help_text='质控图片', null=True, upload_to=mngs.models.upload_to_result),
        ),
    ]
