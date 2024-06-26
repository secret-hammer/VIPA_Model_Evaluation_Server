# Generated by Django 4.2.11 on 2024-05-13 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        ('cv_models', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='architecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.architecture'),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='aspect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.aspect'),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.dataset'),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.environment'),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='parameter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.parameter'),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.task'),
        ),
        migrations.AddField(
            model_name='modelinstance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='instancemetricperspectiverelationship',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.modelinstance'),
        ),
        migrations.AddField(
            model_name='instancemetricperspectiverelationship',
            name='metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.metric'),
        ),
        migrations.AddField(
            model_name='instancemetricperspectiverelationship',
            name='perspective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.perspective'),
        ),
    ]
