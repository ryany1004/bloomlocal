from django.contrib.auth import get_user_model
from django.db import models

from bloom.base import BaseModelMixin


User = get_user_model()


class Order(BaseModelMixin, models.Model):
    total_price = models.FloatField()
    shopper = models.ForeignKey(User, related_name='shopper', on_delete=models.CASCADE)
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


