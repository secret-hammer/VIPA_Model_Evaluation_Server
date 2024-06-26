# Generated by Django 4.2.11 on 2024-05-13 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cv_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('paper_link', models.URLField(blank=True, null=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=True)),
                ('principal', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TaskDatasetRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.dataset')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cv_models.task')),
            ],
        ),
    ]
