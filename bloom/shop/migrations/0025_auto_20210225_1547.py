# Generated by Django 3.1.7 on 2021-02-25 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_product_wp_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='product',
            name='gtin',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='mpn',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]