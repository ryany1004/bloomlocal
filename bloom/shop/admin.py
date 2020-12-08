from django.contrib import admin

from bloom.shop import models


class AttributeValueInline(admin.TabularInline):
    model = models.AttributeValue


@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute_code', 'attribute_name')
    inlines = [
        AttributeValueInline,
    ]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'shop')
