# Generated by Django 4.2.6 on 2024-01-03 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_modelinstance_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelinstance',
            name='scores',
            field=models.CharField(blank=True, default='', max_length=2550, null=True),
        ),
    ]
