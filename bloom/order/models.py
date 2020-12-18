import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models

from bloom.base import BaseModelMixin


User = get_user_model()


class ShippingAddress(models.Model):
    country = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=300)
    street_address_2 = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Order(BaseModelMixin, models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_price = models.FloatField()
    shopper = models.ForeignKey(User, related_name='shopper', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    shopper_share_info = models.BooleanField(default=True)
    shopper_sms_update = models.BooleanField(default=True)

    def __str__(self):
        return "Order: #{}".format(self.id)

    def count_items(self):
        return OrderItem.objects.filter(order_id=self.id).count()


class OrderItem(BaseModelMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    commission_rate = models.FloatField()
    commission_fee = models.FloatField()

    def __str__(self):
        return self.product.title


