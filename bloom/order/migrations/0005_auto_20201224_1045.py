# Generated by Django 3.1.4 on 2020-12-24 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20201218_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='commission_fee',
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='shopper_share_info',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='shopper_sms_update',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='commission_rate',
            field=models.FloatField(default=10),
        ),
    ]