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
    phone_number = models.CharField(max_length=30)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Order(BaseModelMixin, models.Model):
    class Status:
        PENDING = 'pending'
        SUCCEED = 'succeed'
        CANCELED = "canceled"

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('succeed', 'Succeed'),
        ('canceled', 'Canceled'),
        ('failed', 'Failed'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tax = models.FloatField(default=0)
    total_price = models.FloatField()
    shopper = models.ForeignKey(User, related_name='shopper', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    shopper_share_info = models.BooleanField(default=False)
    shopper_sms_update = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=True, default="pending")
    payment_intent = models.CharField(max_length=255, blank=True, editable=False, db_index=True)

    def __str__(self):
        return "Order: #{}".format(self.id)

    def count_items(self):
        return OrderItem.objects.filter(order_id=self.id).count()

    def get_order_id(self):
        return "Order:#{}".format(self.get_order_no())

    def get_order_no(self):
        order_id = "{}".format(self.id)
        return order_id.zfill(6)


class OrderItem(BaseModelMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    commission_rate = models.FloatField(default=10)

    def __str__(self):
        return self.product.title

    def get_merchant_no(self):
        no = "{}".format(self.product.shop.owner_id)
        return no.zfill(2)


