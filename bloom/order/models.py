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
        AWAITING_PAYMENT = 'awaiting_payment'
        PAYMENT_CANCELLED = "payment_cancelled"
        AWAITING_SHIPMENT = 'awaiting_shipment'
        ON_HOLD = 'on_hold'
        SHIPPED = 'shipped'
        CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (Status.AWAITING_PAYMENT, "Awaiting payment"),
        (Status.AWAITING_SHIPMENT, "Awaiting shipment"),
        (Status.PAYMENT_CANCELLED, "Payment cancelled"),
        (Status.ON_HOLD, "On hold"),
        (Status.SHIPPED, "Shipped"),
        (Status.CANCELLED, "Cancelled"),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tax = models.FloatField(default=0)
    total_price = models.FloatField()
    shopper = models.ForeignKey(User, related_name='shopper', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    shopper_share_info = models.BooleanField(default=False)
    shopper_sms_update = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=Status.AWAITING_PAYMENT)
    payment_intent = models.CharField(max_length=255, blank=True, editable=False, db_index=True)

    def __str__(self):
        return "Order: #{}".format(self.id)

    def count_items(self):
        return OrderItem.objects.filter(order_id=self.id).count()

    def get_order_items(self):
        return OrderItem.objects.filter(order_id=self.id)

    def get_order_id(self):
        return "Order:#{}".format(self.get_order_no())

    def get_order_no(self):
        order_id = "{}".format(self.id)
        return order_id.zfill(6)


class OrderItem(BaseModelMixin, models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    color = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    commission_rate = models.FloatField(default=10)

    def __str__(self):
        items = [self.product.title]
        if self.color:
            items.append(self.color)
        if self.size:
            items.append(self.size)
        return " ".join(items)

    def get_merchant_no(self):
        no = "{}".format(self.product.shop.owner_id)
        return no.zfill(2)



