# Generated by Django 3.1.3 on 2021-01-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0002_auto_20210110_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='upload'),
        ),
    ]