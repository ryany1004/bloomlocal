# Generated by Django 3.1.4 on 2021-01-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20201215_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='content_product_id',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
    ]
