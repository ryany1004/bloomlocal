import json

import stripe
from django.conf import settings
from django.db.models.query_utils import Q
from django.utils.dateformat import format
from shipstation.api import ShipStation

from bloom.order.models import OrderItem, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def transfer_to_connected_accounts(order):
    order_items = OrderItem.objects.filter(~Q(product__shop__owner__stripe_account_id=''),
                                           order=order, product__shop__owner__charges_enabled=True) \
        .values('price', 'quantity', 'commission_rate', 'product__shop__owner__stripe_account_id')

    data = {}
    for item in order_items:
        sub_total = item['price'] * item['quantity']
        stripe_fee = sub_total * 0.029 + 0.3
        sub_total = sub_total - stripe_fee
        commission_fee = sub_total * item['commission_rate'] / 100.0
        total = int((sub_total - commission_fee) * 100)

        if item['product__shop__owner__stripe_account_id'] not in data:
            data[item['product__shop__owner__stripe_account_id']] = {'total': total, 'currency': 'usd'}
        else:
            data[item['product__shop__owner__stripe_account_id']]['total'] += total

    for account in data:
        stripe.Transfer.create(amount=data[account]['total'], currency=data[account]['currency'],
                               destination=account, transfer_group=order.get_order_id(),
                               description="Payment for the order #{}".format(order.id))


def send_order_to_ship_station(order: Order):
    ss = ShipStation(key=settings.SHIP_STATION_KEY, secret=settings.SHIP_STATION_SECRET_KEY)
    order_items = []
    items = order.get_order_items()
    for item in items:
        options = []
        if item.color:
            options.append({'name': "Color", "value": item.color})
        if item.size:
            options.append({'name': "Size", "value": item.size})
        order_item = {
            "name": item.__str__(),
            "imageUrl": item.product.thumbnail.url if item.product.thumbnail else None,
            "quantity": item.quantity,
            "unitPrice": item.price,
        }
        if options:
            order_item['options'] = options

        order_items.append(order_item)

    order_obj = {
        "orderNumber": order.get_order_no(),
        "orderKey": str(order.uuid),
        "orderDate": order.created_at.isoformat(),
        "paymentDate": order.created_at.isoformat(),
        "orderStatus": "awaiting_shipment",
        "customerUsername": order.shopper.email if order.shopper_id else order.shipping_address.email,
        "customerEmail": order.shipping_address.email,
        "billTo": {
            "name": order.shopper.get_full_name() if order.shopper_id else None,
        },
        "shipTo": {
            "name": order.shipping_address.__str__(),
            "street1": order.shipping_address.street_address,
            "street2": order.shipping_address.street_address_2,
            "city": order.shipping_address.city,
            "state": order.shipping_address.state,
            "postalCode": order.shipping_address.zip_code,
            "country": order.shipping_address.country,
            "phone": order.shipping_address.phone_number,
            "residential": True
        },
        "items": order_items,

    }
    ss.post(endpoint="/orders/createorder", data=json.dumps(order_obj))
    print("Send order #{} to ShipStation successful".format(order.id))
