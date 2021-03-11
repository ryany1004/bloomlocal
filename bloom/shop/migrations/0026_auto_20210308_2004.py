# Generated by Django 3.1.7 on 2021-03-08 13:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_auto_20210225_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='business_email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='shop',
            name='business_website',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='shop',
            name='delivery_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('delivery', 'Delivery'), ('takeout', 'Takeout'), ('instore_pickup', 'Instore pickup')], max_length=20), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='shop',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='state',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='shop',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='shop',
            name='zipcode',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]