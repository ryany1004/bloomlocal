# Generated by Django 3.1.7 on 2021-02-25 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_create_postgis_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='wp_product_id',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
