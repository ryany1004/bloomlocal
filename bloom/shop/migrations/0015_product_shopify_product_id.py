# Generated by Django 3.1.4 on 2021-01-07 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_product_content_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shopify_product_id',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]