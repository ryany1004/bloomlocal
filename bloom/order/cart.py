import json

from django.conf import settings

from bloom.shop.models import Product


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
                'price': product.price,
                'size': size,
                'color': color,
                'product_id': product.id
            }

        if update_quantity:
            self.cart[product_key]['quantity'] = quantity
        else:
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

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_keys = self.cart.keys()
        product_ids = []
        for key in product_keys:
            product_id = key.split(":")[0]
            if product_id not in product_ids:
                product_ids.append(product_id)

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
        product_keys = self.cart.keys()
        product_ids = []
        for key in product_keys:
            product_id = key.split(":")[0]
            if product_id not in product_ids:
                product_ids.append(product_id)

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
                    'thumbnail': str(product.thumbnail),
                    'shop_name': product.shop.name
                }
            }
            data.append(p)
        return data
