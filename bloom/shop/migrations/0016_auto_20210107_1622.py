# Generated by Django 3.1.4 on 2021-01-07 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_product_shopify_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shopify_product_id',
            field=models.BigIntegerField(blank=True, editable=False, null=True),
        ),
    ]