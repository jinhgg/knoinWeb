# Generated by Django 3.1.4 on 2021-01-13 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mngs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='analys_file_path',
            new_name='analys_file_name',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='sample_file_path',
            new_name='sample_file_name',
        ),
    ]