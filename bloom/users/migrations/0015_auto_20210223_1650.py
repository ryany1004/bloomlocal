# Generated by Django 3.1.4 on 2021-02-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20210126_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopifyapp',
            name='api_key',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='shopifyapp',
            name='config_type',
            field=models.CharField(choices=[('app', 'App'), ('manual', 'Manual')], default='app', max_length=10),
        ),
        migrations.AddField(
            model_name='shopifyapp',
            name='password',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
