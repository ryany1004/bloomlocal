# Generated by Django 3.1.4 on 2020-12-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20201210_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following_shops',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='user',
            name='love_shops',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
