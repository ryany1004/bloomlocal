# Generated by Django 3.1.4 on 2020-12-10 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201207_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='update_at',
            new_name='updated_at',
        ),
    ]
