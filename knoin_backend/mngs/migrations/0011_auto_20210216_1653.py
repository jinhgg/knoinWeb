# Generated by Django 3.1.6 on 2021-02-16 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mngs', '0010_auto_20210205_0820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='collection_id',
        ),
        migrations.AddField(
            model_name='project',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='mngs.collection'),
        ),
    ]
