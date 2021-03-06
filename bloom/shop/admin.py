from django import forms
from django.contrib import admin
from mapwidgets import GooglePointFieldWidget

from bloom.shop import models


@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute_code', 'attribute_name', 'values')


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
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
