from django import forms
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


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'business_address', 'business_phone')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'shop')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


@admin.register(models.ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
