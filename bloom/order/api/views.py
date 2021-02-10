import datetime
import json
import traceback

import django_auto_prefetching
import shopify
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.db.models.functions import ExtractYear
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.order.api.serializers import ShippingAddressSerializer, OrderSerializer, BusinessOrderItemSerializer, \
    BusinessOrderSerializer
from bloom.order.cart import Cart
from bloom.order.models import Order, OrderItem
from bloom.shop.models import Product, Attribute
from bloom.utils.pagination import StandardResultsSetPagination
from bloom.utils.shopping import isdigit


class CartAddAPI(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        product = get_object_or_404(Product, id=data['product_id'], status=0, archived=False)
        cart = Cart(request)
        cart.add(product, quantity=data['quantity'],size=data.get('size'), color=data.get('color'))

        return Response(data=cart.to_json(), status=status.HTTP_200_OK)


class CartRemoveItemAPI(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        product = get_object_or_404(Product, id=data['product_id'])
        cart = Cart(request)
        cart.remove(product, size=data.get('size'), color=data.get('color'))

        return Response(data=cart.to_json(), status=status.HTTP_200_OK)


class CartAPI(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return Response(cart.to_json(), status=status.HTTP_200_OK)


class ValidShippingAddress(APIView):
    def post(self, request, *args, **kwargs):
        data = ShippingAddressSerializer(data=request.data, context={"request": request})
        if data.is_valid():
            pass
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class OrderConfirm(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = ShippingAddressSerializer(data=request.data, context={"request": request})
        if data.is_valid():
            shipping = data.save()
            cart = Cart(request)
            user = request.user if request.user.is_authenticated else None
            order, session = cart.confirm_order(shopper=user, shipping=shipping,
                                                sms_update=request.data['sms_update'],
                                                shopper_share_info=request.data['shopper_share_info'])
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'session': {
                'id': session.id
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OrderDetailsAPI(RetrieveAPIView):
    permission_classes = []

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.role_type == '1':
            return BusinessOrderSerializer
        return OrderSerializer

    def get_object(self):
        order = get_object_or_404(Order.objects.prefetch_related('order_items', "order_items__product", 'order_items__product__shop') \
                                 .select_related('shopper', "shipping_address"), uuid=self.kwargs['uuid'])
        return order


class UserOrderListAPI(django_auto_prefetching.AutoPrefetchViewSetMixin, ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        statuses = [
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.SHIPPED,
            Order.Status.ON_HOLD,
            Order.Status.CANCELLED
        ]
        queryset = Order.objects.prefetch_related('order_items', 'order_items__product', 'order_items__product__shop') \
            .select_related('shopper', 'shipping_address') \
            .filter(shopper=self.request.user, status__in=statuses).order_by('-created_at')
        return django_auto_prefetching.prefetch(queryset, self.serializer_class)


class BusinessMyOrdersAPI(ListAPIView):
    serializer_class = BusinessOrderItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        statuses = [
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.SHIPPED,
            Order.Status.ON_HOLD,
            Order.Status.CANCELLED
        ]
        return OrderItem.objects \
            .select_related('order', 'product', 'product__shop', 'order__shipping_address') \
            .filter(product__shop__owner=self.request.user, order__status__in=statuses).order_by('-order_id')


class ShopifyRetrieveProductAPI(APIView):
    def get(self, request, *args, **kwargs):
        config = request.user.get_shopify_config()
        session = shopify.Session(config.shop_url, settings.SHOPIFY_API_VERSION, config.access_token)
        shopify.ShopifyResource.activate_session(session)
        try:
            products = self.get_all_resources(shopify.Product)
        except Exception as e:
            print(e)
            raise Exception(e)
        finally:
            shopify.ShopifyResource.clear_session()

        return Response(data=products, status=status.HTTP_200_OK)

    def get_all_resources(self, resource, **kwargs):
        # resource_count = resource.count(**kwargs)
        resources = resource.find(limit=250)
        products = []
        for obj in resources:
            draft = json.loads(obj.to_json())['product']
            variants, enable_size, enable_color = self.get_variants(draft)
            images = self.get_images(draft)
            product = {
                'id': draft['id'],
                'title': draft['title'],
                'description': strip_tags(draft.get('body_html') or ''),
                'price': self.get_price(draft),
                'enable_color': enable_color,
                'enable_size': enable_size,
                'status': 0 if draft.get('status') == 'active' else 1,
                'variants': variants,
                'thumbnail': draft['image']['src'] if draft['image'] else None,
                'images': self.get_images(draft),
                'categories': [],
                'stock': self.get_stock(draft)
            }
            products.append(product)
        return products

    def get_price(self, product):
        variants = product.get('variants') or []
        if variants:
            return float(variants[0].get('price') or 0)
        return 0

    def get_stock(self, product):
        variants = product.get('variants') or []
        if variants:
            return variants[0].get('inventory_quantity') or 0
        return 0

    def get_images(self, product):
        images = []
        for img in (product.get('images') or []):
            if img['src']:
                images.append(img['src'])

        return [{'src': img} for img in images]

    def get_variants(self, product):
        enable_color = False
        enable_size = False
        variants = []
        options = product.get('options') or []
        var_objs = product.get('variants') or []

        attr_size = Attribute.objects.get(attribute_code='size')
        attr_color = Attribute.objects.get(attribute_code='color')

        size_option = None
        color_option = None
        count = 1
        for opt in options:
            if opt['name'] == "Size":
                for v in opt['values']:
                    if v not in attr_size.values:
                        attr_size.values.append(v)
                attr_size.save()
                size_option = 'option{}'.format(count)
            elif opt['name'] == "Color":
                for v in opt['values']:
                    if v.capitalize() not in attr_color.values:
                        attr_color.values.append(v.capitalize())
                attr_color.save()
                color_option = 'option{}'.format(count)
            count += 1

        prices = {}
        for v in var_objs:
            price = float(v['price']) if v['price'] and isdigit(v['price']) else None
            price = price if price and price > 0 else None
            if size_option and color_option:
                key = "{}:{}".format(v[size_option], v[color_option])
                prices[key] = price
            elif size_option:
                prices[v[size_option]] = price
            elif color_option:
                prices[v[color_option]] = price

        if len(options) == 1:
            option = options[0]
            if option['name'] == "Color":
                enable_color = True
                values = option['values']
                for v in values:
                    variants.append({'color': v.capitalize(), 'price': prices.get(v)})
            elif option['name'] == "Size":
                enable_size = True
                values = option['values']
                for v in values:
                    variants.append({'size': v, 'price': prices.get(v)})
        elif len(options) > 1:
            size_values = []
            color_values = []
            for option in options:
                if option['name'] == "Color":
                    color_values = option['values']
                    enable_color = True
                if option['name'] == "Size":
                    enable_size = True
                    size_values = option['values']

            if len(size_values) > 0 and len(color_values) > 0:
                for size in size_values:
                    for color in color_values:
                        key = "{}:{}".format(size, color)
                        variants.append({"size": size, "color": color.capitalize(), 'price': prices.get(key)})
            elif len(size_values) > 0:
                for size in size_values:
                    variants.append({"size": size, 'price': prices.get(size)})
            elif len(color_values) > 0:
                for color in color_values:
                    variants.append({"color": color.capitalize(), 'price': prices.get(color)})

        return variants, enable_size, enable_color


class OrderRevenueMonthAPI(APIView):

    def get(self, request, *args, **kwargs):
        this_month = datetime.date.today()
        prev_month = this_month - relativedelta(months=1)
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__month=this_month.month,
                                         created_at__year=this_month.year)

        prev_month_items = OrderItem.objects.filter(order__status__in=statuses,
                                                    product__shop__owner=request.user,
                                                    created_at__month=prev_month.month,
                                                    created_at__year=prev_month.year)

        total_orders_this_month = items.values('order').distinct().count()
        total_orders_prev_month = prev_month_items.values('order').distinct().count()

        total_revenue_this_month = items.aggregate(
            total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0
        total_revenue_prev_month = prev_month_items.aggregate(
            total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0
        data = {
            'this_month': {
                'total_orders': total_orders_this_month,
                'revenue': total_revenue_this_month
            },
            'previous_month': {
                'total_orders': total_orders_prev_month,
                'revenue': total_revenue_prev_month
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OrderRevenueYearAPI(APIView):
    def get(self, request, *args, **kwargs):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user)
        data = items.annotate(year=ExtractYear("created_at")).values('year') \
            .annotate(total=Sum(F("price") * F("quantity"), output_field=models.FloatField()))

        return Response(data=list(data), status=status.HTTP_200_OK)
