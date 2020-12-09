from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.contrib.postgres import fields
from django.db import models
from django.db.models.fields.json import JSONField

from bloom.base import BaseModelMixin
from bloom.utils.paths import get_photo_path

User = get_user_model()


class Integration(models.Model):
    status = models.CharField(max_length=20, blank=True)
    key = models.CharField(max_length=50, blank=True)


class Shop(BaseModelMixin, models.Model):
    STORE_TYPES = (
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('electronics', 'Electronics'),
    )

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_set')
    business_address = models.CharField(max_length=255, blank=True)
    business_phone = models.CharField(max_length=20, blank=True)
    store_type = models.CharField(max_length=20, blank=True, choices=STORE_TYPES)
    tax_id = models.CharField(max_length=20, blank=True)
    integrations = JSONField(default=list, blank=True)
    locality = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(BaseModelMixin, models.Model):
    DELIVERY_TYPES = (
        ('pickup', "Pickup"),
        ('delivery', "Delivery"),
        ('both', "Both"),
    )
    STATUS_CHOICES = (
        (0, "Active"),
        (1, "Deactivate"),
    )
    title = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True, db_index=True)
    price = models.FloatField()
    thumbnail = models.ImageField(upload_to=get_photo_path)
    description = models.TextField(blank=True)
    length = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    dimension_unit = models.CharField(max_length=10)
    weight = models.FloatField()
    weight_unit = models.CharField(max_length=10)
    stock = models.IntegerField(null=True, blank=True)
    delivery_type = models.CharField(max_length=10)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    rating = models.FloatField(default=0)
    categories = models.ManyToManyField(Category, blank=True)
    enable_color = models.BooleanField(default=True)
    enable_size = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0, blank=True)
    quantity_per_unit = models.CharField(max_length=20, blank=True)
    unit_price = models.CharField(max_length=20, blank=True)
    shipment_id = models.IntegerField(blank=True, null=True)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_image_url(self):
        if not self.image:
            return None
        return self.image.url

    def get_product_images(self):
        return ProductImage.objects.filter(product_id=self.id).values_list('image')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = JSONField(default=list, blank=True)

    def get_image_url(self):
        if not self.image:
            return None
        return self.image.url


class ProductRating(BaseModelMixin, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    content = models.TextField(blank=True)


class Attribute(models.Model):
    attribute_code = models.CharField(max_length=20, primary_key=True)
    attribute_name = models.CharField(max_length=20)

    def __str__(self):
        return self.attribute_name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=20, null=True, help_text="These changes affect all related products.")
    text = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.text


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    """{
        data: {
        }
    }"""
    values = JSONField(default=list)
