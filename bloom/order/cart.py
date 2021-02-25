import stripe
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import transaction
from django.urls import reverse

from bloom.analytics.api.views import product_added_to_cart_log
from bloom.order.models import Order, OrderItem
from bloom.shop.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, size=None, color=None, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_key = "{}:{}:{}".format(product.id, size, color)
        if product_key not in self.cart:
            self.cart[product_key] = {
                'quantity': 0,
                'price': product.get_product_price(size, color),
                'size': size,
                'color': color,
                'product_id': product.id
            }

        if update_quantity:
            self.cart[product_key]['quantity'] = quantity
        else:
            if self.cart[product_key]['quantity'] == 0:
                product_added_to_cart_log(product)
            self.cart[product_key]['quantity'] += quantity
        self.save()

    def save(self):
        """
        mark the session as "modified" to make sure it gets saved
        """
        self.session.modified = True

    def remove(self, product, size=None, color=None):
        """
        Remove a product from the cart.
        """
        product_key = "{}:{}:{}".format(product.id, size, color)
        if product_key in self.cart:
            del self.cart[product_key]
            self.save()

    def get_product_ids(self):
        product_keys = self.cart.keys()
        product_ids = []
        for key in product_keys:
            product_id = key.split(":")[0]
            if product_id not in product_ids:
                product_ids.append(product_id)

        return product_ids

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.get_product_ids()

        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for item in cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        calculate the total cost of the items in the cart
        """
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        remove cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price_after_discount(self):
        return self.get_total_price()

    def to_json(self):
        product_ids = self.get_product_ids()

        # get the product objects and add them to the cart
        products = Product.objects.select_related('shop').filter(id__in=product_ids)
        map_products = {}
        for p in products:
            map_products[p.id] = p

        data = []

        for item in self.cart.values():
            product = map_products[item['product_id']]
            p = {
                'quantity': item['quantity'],
                'price': item['price'],
                'size': item['size'],
                'color': item['color'],
                'product': {
                    'id': product.id,
                    'uuid': str(product.uuid),
                    'title': product.title,
                    'slug': product.slug,
                    'url': product.get_absolute_url(),
                    'thumbnail': str(product.thumbnail),
                    'shop_name': product.shop.name
                }
            }
            data.append(p)
        return data

    @transaction.atomic
    def confirm_order(self, shopper=None, shipping=None, sms_update=False, shopper_share_info=False):
        order = Order()
        order.shipping_address = shipping
        order.shopper = shopper
        order.shopper_share_info = shopper_share_info
        order.shopper_sms_update = sms_update
        order.total_price = self.get_total_price()
        order.save()

        product_ids = self.get_product_ids()
        # get the product objects and add them to the cart
        products = Product.objects.select_related('shop').filter(id__in=product_ids)
        map_products = {}
        for p in products:
            map_products[p.id] = p

        items = []
        checkout_items = []
        for obj in self.cart.values():
            product = map_products[obj['product_id']]
            item = OrderItem()
            item.order = order
            item.price = product.price
            item.product = product
            item.color = obj['color']
            item.size = obj['size']
            item.quantity = obj['quantity']
            items.append(item)

            obj = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.title,
                        'images': [product.thumbnail.url]
                    },
                    "unit_amount": int(product.price * 100)
                },
                'quantity': item.quantity
            }
            if product.description:
                obj['price_data']['product_data']['description'] = product.description
            checkout_items.append(obj)

        OrderItem.objects.bulk_create(items)
        # session = self.create_session(checkout_items, order)
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_price * 100),
            currency="usd",
            transfer_group=order.get_order_id(),
            description="Payment for the order #{}".format(order.id),
            shipping={
                "address": {
                    'line1': shipping.street_address,
                    'city': shipping.city,
                    'country': shipping.country,
                    'state': shipping.state,
                    'postal_code': shipping.zip_code
                },
                "name": "{} {}".format(shipping.first_name, shipping.last_name) ,
                "phone": shipping.phone_number,
            }
        )
        order.payment_intent = intent.id
        order.save()

        site = Site.objects.get_current()
        domain = "{}://{}".format('https' if settings.SECURE_SSL_REDIRECT else "http", site.domain)
        success_url = domain + reverse("order:order-success", kwargs={'uuid': order.uuid})
        cancel_url = domain + reverse("order:order-canceled", kwargs={'uuid': order.uuid})

        return order, intent, success_url, cancel_url

    def create_session(self, items, order):
        site = Site.objects.get_current()
        domain = "{}://{}".format('https' if settings.SECURE_SSL_REDIRECT else "http", site.domain)
        success_url = domain + reverse("order:order-success", kwargs={'uuid': order.uuid})
        cancel_url = domain + reverse("order:order-canceled", kwargs={'uuid': order.uuid})
        session = stripe.checkout.Session.create(payment_method_types=['card'],
                                                 line_items=items,
                                                 mode='payment',
                                                 success_url=success_url,
                                                 cancel_url=cancel_url,
                                                 payment_intent_data={
                                                     'transfer_group': order.get_order_id(),
                                                     "description": "Payment for the order #{}".format(order.id)
                                                 })
        order.payment_intent = session.payment_intent
        order.save()
        return session

