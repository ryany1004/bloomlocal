import datetime
import json

from dateutil.relativedelta import relativedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.aggregates import Sum, Count, Avg
from django.db.models.expressions import F
from django.db.models.functions import Trunc
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.analytics.api.serializers import StorefrontViewSerializer, ProductViewSerializer
from bloom.analytics.models import StorefrontView, ProductView, ProductAddedToCart
from bloom.order.models import Order, OrderItem
from bloom.shop.api.serializers import ProductModelSimpleSerializer
from bloom.shop.models import Shop, Product


class StorefrontViewAPI(CreateAPIView):
    serializer_class = StorefrontViewSerializer
    permission_classes = []

    def perform_create(self, serializer):
        shop = get_object_or_404(Shop, uuid=self.kwargs['uuid'])
        obj, created = StorefrontView.objects.get_or_create(shop=shop,
                                                            viewed_date=datetime.date.today())
        StorefrontView.objects.filter(id=obj.id).update(count=F('count') + 1)
        obj.refresh_from_db()
        return obj


class ProductViewAPI(CreateAPIView):
    serializer_class = ProductViewSerializer
    permission_classes = []

    def perform_create(self, serializer):
        product = get_object_or_404(Product, uuid=self.kwargs['uuid'])
        channel = self.request.data['channel']
        obj, created = ProductView.objects.get_or_create(product=product,
                                                         viewed_date=datetime.date.today(),
                                                         channel=channel)
        ProductView.objects.filter(id=obj.id).update(count=F('count') + 1)
        obj.refresh_from_db()
        return obj


def product_added_to_cart_log(product):
    obj = ProductAddedToCart.objects.get_or_create(product=product,
                                                   added_date=datetime.date.today())[0]

    ProductAddedToCart.objects.filter(id=obj.id).update(count=F('count') + 1)


class StorefrontViewData(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_views_by_month(shop)
        else:
            data = self.get_views_by_days(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_views_by_month(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

        kwargs = {
            'viewed_date__month': this_month.month,
            'created_at__year': this_month.year,
        }
        this_month_count = StorefrontView.objects.filter(shop=shop,
                                                         viewed_date__month=this_month.month,
                                                         viewed_date__year=this_month.year) \
            .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0
        last_month_count = StorefrontView.objects.filter(shop=shop,
                                                         viewed_date__month=last_month.month,
                                                         viewed_date__year=last_month.year) \
            .aggregate(last_month_count=Sum('count'))['last_month_count'] or 0
        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_views_by_days(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1) - relativedelta(days=this_month.day) + relativedelta(days=1)
        objs = StorefrontView.objects.filter(shop=shop,
                                             viewed_date__gte=last_month) \
            .values('viewed_date', 'count')
        return list(objs)


class ProductViewData(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_views_by_month(shop)
        else:
            data = self.get_views_by_days(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_views_by_month(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

        kwargs = {
            'viewed_date__month': this_month.month,
            'created_at__year': this_month.year,
        }
        this_month_count = ProductView.objects.filter(
            product__shop=shop,
            viewed_date__month=this_month.month,
            viewed_date__year=this_month.year) \
            .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0
        last_month_count = ProductView.objects.filter(product__shop=shop,
                                                      viewed_date__month=last_month.month,
                                                      viewed_date__year=last_month.year) \
            .aggregate(last_month_count=Sum('count'))['last_month_count'] or 0
        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_views_by_days(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1) - relativedelta(days=this_month.day) + relativedelta(days=1)
        objs = ProductView.objects.filter(
            product__shop=shop,
            viewed_date__gte=last_month).values('viewed_date') \
            .annotate(total_view=Sum('count')) \
            .values('viewed_date', 'total_view')
        return list(objs)


class ProductAddedToCartData(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_views_by_month(shop)
        else:
            data = self.get_views_by_days(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_views_by_month(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

        kwargs = {
            'viewed_date__month': this_month.month,
            'created_at__year': this_month.year,
        }
        this_month_count = ProductAddedToCart.objects.filter(
            product__shop=shop,
            added_date__month=this_month.month,
            added_date__year=this_month.year) \
            .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0
        last_month_count = ProductAddedToCart.objects.filter(
            product__shop=shop,
            added_date__month=last_month.month,
            added_date__year=last_month.year) \
            .aggregate(last_month_count=Sum('count'))['last_month_count'] or 0
        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_views_by_days(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1) - relativedelta(days=this_month.day) + relativedelta(days=1)
        objs = ProductAddedToCart.objects.filter(
            product__shop=shop,
            added_date__gte=last_month).values('added_date') \
            .annotate(total_view=Sum('count')) \
            .values('added_date', 'total_view')
        return list(objs)


class ShopRevenueData(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_data_by_month(request, shop)
        else:
            data = self.get_data_by_days(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_data_by_month(self, request, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__month=this_month.month,
                                         created_at__year=this_month.year)

        last_month_items = OrderItem.objects.filter(order__status__in=statuses,
                                                    product__shop__owner=request.user,
                                                    created_at__month=last_month.month,
                                                    created_at__year=last_month.year)

        revenue_this_month = items.aggregate(
            total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0
        revenue_last_month = last_month_items.aggregate(
            total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0
        return {
            'this_month': revenue_this_month,
            'last_month': revenue_last_month
        }

    def get_data_by_days(self, request, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1) - relativedelta(days=this_month.day) + relativedelta(days=1)

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__gte=last_month) \
            .annotate(day=Trunc('order__created_at', 'day', output_field=models.DateField())) \
            .values('day').annotate(total=Sum(F("price") * F('quantity'), output_field=models.FloatField())) \
            .values('day', 'total').order_by('day')
        return list(items)


class ShopOrderData(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_data_by_month(request, shop)
        else:
            data = self.get_data_by_days(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_data_by_month(self, request, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__month=this_month.month,
                                         created_at__year=this_month.year)

        last_month_items = OrderItem.objects.filter(order__status__in=statuses,
                                                    product__shop__owner=request.user,
                                                    created_at__month=last_month.month,
                                                    created_at__year=last_month.year)

        total_orders_this_month = items.values('order').distinct().count()
        total_orders_last_month = last_month_items.values('order').distinct().count()

        return {
            'this_month': total_orders_this_month,
            'last_month': total_orders_last_month
        }

    def get_data_by_days(self, request, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1) - relativedelta(days=this_month.day) + relativedelta(days=1)

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__gte=last_month) \
            .annotate(day=Trunc('order__created_at', 'day', output_field=models.DateField())) \
            .values('day').annotate(total=Count('order', distinct=True)) \
            .values('day', 'total').order_by('day')
        return list(items)


class ShopPopularProductsData(ListAPIView):
    serializer_class = ProductModelSimpleSerializer

    def get_queryset(self):
        shop = self.request.user.get_shop()
        view_product_ids = ProductView.objects.filter(product__shop=shop) \
                               .values('product').annotate(total=Sum('count')) \
                               .order_by('-total').values_list('product', flat=True)[:10]

        sale_product_id = OrderItem.objects.filter(product__shop=shop) \
                              .values('product').annotate(total=Count("*")) \
                              .order_by('-total').values_list('product', flat=True)[:10]

        product_ids = list(view_product_ids) + list(sale_product_id)
        return Product.objects.filter(id__in=product_ids)


class SalePieChartData(APIView):
    def get(self, request, *args, **kwargs):
        from dateutil.parser import parse
        shop = self.request.user.get_shop()
        try:
            filter_date = parse(request.GET.get('month'), yearfirst=True)
        except:
            filter_date = datetime.date.today()

        data = OrderItem.objects.filter(product__shop=shop,
                                        created_at__year=filter_date.year,
                                        created_at__month=filter_date.month).values('order__source') \
            .annotate(count=Count('*')).values('order__source', 'count')

        total = OrderItem.objects.filter(product__shop=shop) \
            .values('order').distinct().count()
        results = []
        source_map = dict(Order.SOURCE_CHOICES)
        labels = []
        values = []
        titles = []
        for obj in data:
            value = round(obj['count'] / total * 100, 0)
            label = source_map.get(obj['order__source'], obj['order__source'])
            title = '{}% {}'.format(value, label)
            labels.append(label)
            values.append(value)
            titles.append(title)

        return Response(data={
            'labels': labels,
            'data': values,
            'titles': titles
        }, status=status.HTTP_200_OK)


class OtherDataReport(APIView):
    def get(self, request, *args, **kwargs):
        shop = self.request.user.get_shop()
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        avg_order_amount = OrderItem.objects.filter(product__shop=shop,
                                                    order__status__in=statuses).values('order') \
            .annotate(total=Sum(F("price") * F('quantity'), output_field=models.FloatField())) \
            .aggregate(avg_amount=Avg('total'))['avg_amount'] or 0

        avg_product_per_order = OrderItem.objects.filter(product__shop=shop,
                                                         order__status__in=statuses).values('order') \
            .annotate(total=Count("product")) \
            .aggregate(avg_num_product=Avg('total'))['avg_num_product'] or 0

        return Response(data={
            'avg_order_amount': round(avg_order_amount, 0),
            'avg_product_per_order': round(avg_product_per_order, 1)
        }, status=status.HTTP_200_OK)


