# Generated by Django 3.1.4 on 2020-12-09 02:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201208_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='shop',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='values',
            field=models.JSONField(default=list),
        ),
    ]
