# Generated by Django 3.1.4 on 2020-12-24 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20201224_1050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='phone',
            new_name='phone_number',
        ),
    ]