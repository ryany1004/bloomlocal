# Generated by Django 3.1.4 on 2020-12-08 03:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0004_auto_20201207_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='image',
        ),
        migrations.AddField(
            model_name='productimage',
            name='images',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='shop',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
