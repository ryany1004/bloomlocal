import stripe
from django.conf import settings
from django.db.models.query_utils import Q

from bloom.order.models import OrderItem


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

