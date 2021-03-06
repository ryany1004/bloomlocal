# Generated by Django 3.1.4 on 2021-01-09 10:13

from django.db import migrations

SIZES = {
    'extra_small': 'Extra small',
    'small': 'Small',
    'medium': 'Medium',
    'large': 'Large',
    'extra_large': 'Extra large',
}
COLORS = {
    "red": "Red",
    "green": "Green",
    "blue": "Blue",
    "black": "Black",
    "white": "White",
    "gray": "Gray",
}


def fix_data_product(apps, schema_editor):
    OrderItem = apps.get_model('order', "OrderItem")
    items = OrderItem.objects.all()
    for item in items.iterator():
        if item.size:
            item.size = SIZES[item.size]

        if item.color:
            item.color = COLORS[item.color]
        item.save()

    ProductVariant = apps.get_model("shop", "ProductVariant")
    variants = ProductVariant.objects.all()
    for variant in variants.iterator():
        for value in variant.values:
            if 'size' in value:
                value['size'] = SIZES[value['size']]

            if 'color' in value:
                value['color'] = COLORS[value['color']]
        variant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20201228_1149'),
        ('shop', '0018_auto_20210109_1713'),
    ]

    operations = [
        migrations.RunPython(fix_data_product)
    ]
