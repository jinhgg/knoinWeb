# Generated by Django 3.1.4 on 2021-01-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mngs', '0008_auto_20210128_0604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='results_zip_file',
        ),
        migrations.AddField(
            model_name='collection',
            name='results_zip_path',
            field=models.CharField(blank=True, help_text='分析结果zip文件路径', max_length=150, null=True),
        ),
    ]
