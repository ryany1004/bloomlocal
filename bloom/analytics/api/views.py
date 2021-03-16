import datetime
import json

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.aggregates import Sum, Count, Avg
from django.db.models.expressions import F, OuterRef, Subquery, Value
from django.db.models.functions import Trunc, ExtractWeek, Concat, ExtractYear, ExtractMonth
from django.utils.dateformat import format
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
            data = self.get_month_data(shop)
        if request.GET.get('type') == 'by_week':
            data = self.get_data_by_week(shop)
        elif request.GET.get('type') == 'by_month':
            data = self.get_data_by_month(shop)
        else:
            data = self.get_data_by_day(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_month_data(self, shop):
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

        if settings.ENABLE_DUMMY_DATA:
            return {
                'this_month': 150,
                'last_month': 88
            }
        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_data_by_day(self, shop):
        objs = StorefrontView.objects.filter(shop=shop) \
            .annotate(total_view=F('count')) \
            .values('viewed_date', 'total_view')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"viewed_date": "2021-02-10", "total_view": 9}, {"viewed_date": "2021-02-10", "total_view": 7},
                    {"viewed_date": "2021-02-10", "total_view": 4}, {"viewed_date": "2021-02-09", "total_view": 1},
                    {"viewed_date": "2021-02-17", "total_view": 1}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                data[count]['viewed_date'] = format("Y-m-d", today - relativedelta(days=i))
                count += 1
            return data

        return list(objs)

    def get_data_by_week(self, shop):
        objs = StorefrontView.objects.filter(shop=shop) \
            .annotate(
                day_year=ExtractYear('viewed_date'),
                day_week=ExtractWeek('viewed_date')) \
            .values('day_year', 'day_week') \
            .annotate(total_view=Sum("count")) \
            .values('day_year', 'day_week', 'total_view').order_by('day_year', 'day_week')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-10", "total_view": 9}, {"day_year": "2021-02-10", "total_view": 7},
                    {"day_year": "2021-02-10", "total_view": 4}, {"day_year": "2021-02-09", "total_view": 1},
                    {"day_year": "2021-02-17", "total_view": 1}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(weeks=i)
                data[count]['day_year'] = day.year
                data[count]['day_week'] = day.isocalendar()[1]
                count += 1
            return data

        return list(objs)

    def get_data_by_month(self, shop):
        objs = StorefrontView.objects.filter(shop=shop) \
            .annotate(
                day_year=ExtractYear('viewed_date'),
                day_month=ExtractMonth('viewed_date')) \
            .values('day_year', 'day_month') \
            .annotate(total_view=Sum("count")) \
            .values('day_year', 'day_month', 'total_view').order_by('day_year', 'day_month')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-10", "total_view": 9}, {"day_year": "2021-02-10", "total_view": 7},
                    {"day_year": "2021-02-10", "total_view": 4}, {"day_year": "2021-02-09", "total_view": 1},
                    {"day_year": "2021-02-17", "total_view": 1}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(months=i)
                data[count]['day_year'] = day.year
                data[count]['day_month'] = day.month
                count += 1
            return data

        return list(objs)


class ProductViewData(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_month_data(shop)
        if request.GET.get('type') == 'by_week':
            data = self.get_data_by_week(shop)
        elif request.GET.get('type') == 'by_month':
            data = self.get_data_by_month(shop)
        else:
            data = self.get_data_by_day(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_month_data(self, shop):
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

        if settings.ENABLE_DUMMY_DATA:
            return {
                'this_month': 210,
                'last_month': 110
            }

        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_data_by_day(self, shop):
        objs = ProductView.objects.filter(
                product__shop=shop).values('viewed_date') \
            .annotate(total_view=Sum('count')) \
            .values('viewed_date', 'total_view')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"viewed_date": "2021-02-11", "total_view": 5}, {"viewed_date": "2021-02-12", "total_view": 3},
                    {"viewed_date": "2021-02-10", "total_view": 6}, {"viewed_date": "2021-02-09", "total_view": 2}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                data[count]['viewed_date'] = format("Y-m-d", today - relativedelta(days=i))
                count += 1
            return data

        return list(objs)

    def get_data_by_week(self, shop):
        objs = ProductView.objects.filter(
                product__shop=shop) \
            .annotate(
                day_year=ExtractYear('viewed_date'),
                day_week=ExtractWeek('viewed_date')) \
            .values('day_year', 'day_week') \
            .annotate(total_view=Sum('count')) \
            .values('day_year', 'day_week', 'total_view').order_by('day_year', 'day_week')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-11", "total_view": 5}, {"day_year": "2021-02-12", "total_view": 3},
                    {"day_year": "2021-02-11", "total_view": 8}, {"day_year": "2021-02-12", "total_view": 6},
                    {"day_year": "2021-02-10", "total_view": 6}, {"day_year": "2021-02-09", "total_view": 2}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(weeks=i)
                data[count]['day_year'] = day.year
                data[count]['day_week'] = day.isocalendar()[1]
                count += 1
            return data

        return list(objs)

    def get_data_by_month(self, shop):
        objs = ProductView.objects.filter(
                product__shop=shop) \
            .annotate(
                day_year=ExtractYear('viewed_date'),
                day_month=ExtractMonth('viewed_date')) \
            .values('day_year', 'day_month') \
            .annotate(total_view=Sum('count')) \
            .values('day_year', 'day_month', 'total_view').order_by('day_year', 'day_month')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-11", "total_view": 5}, {"day_year": "2021-02-12", "total_view": 3},
                    {"day_year": "2021-02-11", "total_view": 8}, {"day_year": "2021-02-12", "total_view": 6},
                    {"day_year": "2021-02-10", "total_view": 6}, {"day_year": "2021-02-09", "total_view": 2}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(months=i)
                data[count]['day_year'] = day.year
                data[count]['day_month'] = day.month
                count += 1
            return data

        return list(objs)


class ProductViewChannelsData(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_month_data(shop)
        if request.GET.get('type') == 'by_week':
            data = self.get_data_by_week(shop)
        elif request.GET.get('type') == 'by_month':
            data = self.get_data_by_month(shop)
        else:
            data = self.get_data_by_day(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_month_data(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

        kwargs = {
            'viewed_date__month': this_month.month,
            'created_at__year': this_month.year,
        }
        this_month_count = ProductView.objects.filter(
            product__shop=shop,
            viewed_date__month=this_month.month,
            viewed_date__year=this_month.year).exclude(channel='website') \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0
        last_month_count = ProductView.objects.filter(product__shop=shop,
                                                      viewed_date__month=last_month.month,
                                                      viewed_date__year=last_month.year) \
                               .aggregate(last_month_count=Sum('count'))['last_month_count'] or 0

        if settings.ENABLE_DUMMY_DATA:
            return {
                'this_month': 120,
                'last_month': 90
            }

        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_data_by_day(self, shop):
        objs = ProductView.objects.filter(
            product__shop=shop) \
            .values('viewed_date').exclude(channel='website') \
            .annotate(total_view=Sum('count')) \
            .values('viewed_date', 'total_view')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"viewed_date": "2021-02-11", "total_view": 3}, {"viewed_date": "2021-02-12", "total_view": 7},
                    {"viewed_date": "2021-02-10", "total_view": 1}, {"viewed_date": "2021-02-09", "total_view": 2}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                data[count]['viewed_date'] = format("Y-m-d", today - relativedelta(days=i))
                count += 1
            return data

        return list(objs)

    def get_data_by_week(self, shop):
        objs = ProductView.objects.filter(
            product__shop=shop) \
            .annotate(
                day_year=ExtractYear('viewed_date'),
                day_week=ExtractWeek('viewed_date')) \
            .values('day_year', 'day_week').exclude(channel='website') \
            .annotate(total_view=Sum('count')) \
            .values('day_year', 'day_week', 'total_view').order_by('day_year', 'day_week')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"viewed_date": "2021-02-11", "total_view": 3}, {"viewed_date": "2021-02-12", "total_view": 7},
                    {"viewed_date": "2021-02-10", "total_view": 1}, {"viewed_date": "2021-02-09", "total_view": 2}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(weeks=i)
                data[count]['day_year'] = day.year
                data[count]['day_week'] = day.isocalendar()[1]
                count += 1
            return data

        return list(objs)

    def get_data_by_month(self, shop):
        objs = ProductView.objects.filter(
            product__shop=shop) \
            .annotate(
                day_year=ExtractYear('viewed_date'),
                day_month=ExtractMonth('viewed_date')) \
            .values('day_year', 'day_month').exclude(channel='website') \
            .annotate(total_view=Sum('count')) \
            .values('day_year', 'day_month', 'total_view').order_by('day_year', 'day_month')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-11", "total_view": 3}, {"day_year": "2021-02-12", "total_view": 7},
                    {"day_year": "2021-02-11", "total_view": 6}, {"day_year": "2021-02-12", "total_view": 7},
                    {"day_year": "2021-02-10", "total_view": 1}, {"day_year": "2021-02-09", "total_view": 2}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(months=i)
                data[count]['day_year'] = day.year
                data[count]['day_month'] = day.month
                count += 1
            return data

        return list(objs)


class ProductAddedToCartData(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_month_data(shop)
        if request.GET.get('type') == 'by_week':
            data = self.get_data_by_week(shop)
        elif request.GET.get('type') == 'by_month':
            data = self.get_data_by_month(shop)
        else:
            data = self.get_data_by_day(shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_month_data(self, shop):
        this_month = datetime.date.today()
        last_month = this_month - relativedelta(months=1)

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

        if settings.ENABLE_DUMMY_DATA:
            return {
                'this_month': 80,
                'last_month': 44
            }
        return {
            'this_month': this_month_count,
            'last_month': last_month_count
        }

    def get_data_by_day(self, shop):
        objs = ProductAddedToCart.objects.filter(
            product__shop=shop).values('added_date') \
            .annotate(total_view=Sum('count')) \
            .values('added_date', 'total_view').order_by('added_date')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"added_date": "2021-02-11", "total_view": 2}, {"added_date": "2021-02-13", "total_view": 2},
                    {"added_date": "2021-02-12", "total_view": 4}, {"added_date": "2021-02-10", "total_view": 3},
                    {"added_date": "2021-02-09", "total_view": 3}, {"added_date": "2021-02-17", "total_view": 3}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                data[count]['added_date'] = format("Y-m-d", today - relativedelta(days=i))
                count += 1
            return data

        return list(objs)

    def get_data_by_week(self, shop):
        objs = ProductAddedToCart.objects.filter(
            product__shop=shop) \
            .annotate(
                day_year=ExtractYear('added_date'),
                day_week=ExtractWeek('added_date')) \
            .values('day_year', 'day_week') \
            .annotate(total_view=Sum('count')) \
            .values('day_year', 'day_week', 'total_view').order_by('day_year', 'day_week')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-11", "total_view": 2}, {"day_year": "2021-02-13", "total_view": 2},
                    {"day_year": "2021-02-12", "total_view": 4}, {"day_year": "2021-02-10", "total_view": 3},
                    {"day_year": "2021-02-09", "total_view": 3}, {"day_year": "2021-02-17", "total_view": 3}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(weeks=i)
                data[count]['day_year'] = day.year
                data[count]['day_week'] = day.isocalendar()[1]
                count += 1
            return data

        return list(objs)

    def get_data_by_month(self, shop):
        objs = ProductAddedToCart.objects.filter(
            product__shop=shop) \
            .annotate(
                day_year=ExtractYear('added_date'),
                day_month=ExtractMonth('added_date')) \
            .values('day_year', 'day_month') \
            .annotate(total_view=Sum('count')) \
            .values('day_year', 'day_month', 'total_view').order_by('day_year', 'day_month')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-02-11", "total_view": 2}, {"day_year": "2021-02-13", "total_view": 2},
                    {"day_year": "2021-02-12", "total_view": 4}, {"day_year": "2021-02-10", "total_view": 3},
                    {"day_year": "2021-02-09", "total_view": 3}, {"day_year": "2021-02-17", "total_view": 3}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(months=i)
                data[count]['day_year'] = day.year
                data[count]['day_month'] = day.month
                count += 1
            return data

        return list(objs)

class ShopRevenueData(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_month_data(request, shop)
        if request.GET.get('type') == 'by_week':
            data = self.get_data_by_week(request, shop)
        elif request.GET.get('type') == 'by_month':
            data = self.get_data_by_month(request, shop)
        else:
            data = self.get_data_by_day(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_month_data(self, request, shop):
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

        if settings.ENABLE_DUMMY_DATA:
            return {
                'this_month': 625,
                'last_month': 260
            }
        return {
            'this_month': revenue_this_month,
            'last_month': revenue_last_month
        }

    def get_data_by_day(self, request, shop):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user) \
            .annotate(day=Trunc('order__created_at', 'day', output_field=models.DateField())) \
            .values('day').annotate(total=Sum(F("price") * F('quantity'), output_field=models.FloatField())) \
            .values('day', 'total').order_by('day')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day": "2021-01-06", "total": 50.0}, {"day": "2021-01-09", "total": 10.0},
                    {"day": "2021-01-12", "total": 90.0}, {"day": "2021-01-13", "total": 70.0},
                    {"day": "2021-01-15", "total": 80.0}, {"day": "2021-01-22", "total": 22.0},
                    {"day": "2021-02-17", "total": 25.0}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                data[count]['day'] = format("Y-m-d", today - relativedelta(days=i))
                count += 1
            return data

        return list(items)

    def get_data_by_week(self, request, shop):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user) \
            .annotate(
                day_year=ExtractYear('order__created_at'),
                day_week=ExtractWeek('order__created_at')) \
            .values('day_year', 'day_week') \
            .annotate(total=Sum(F("price") * F('quantity'), output_field=models.FloatField())) \
            .values('day_year', 'day_week', 'total').order_by('day_year', 'day_week')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-01-06", "total": 50.0}, {"day_year": "2021-01-09", "total": 10.0},
                    {"day_year": "2021-01-12", "total": 90.0}, {"day_year": "2021-01-13", "total": 70.0},
                    {"day_year": "2021-01-15", "total": 80.0}, {"day_year": "2021-01-22", "total": 22.0},
                    {"day_year": "2021-02-17", "total": 25.0}]

            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(weeks=i)
                data[count]['day_year'] = day.year
                data[count]['day_week'] = day.isocalendar()[1]
                count += 1
            return data

        return list(items)

    def get_data_by_month(self, request, shop):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user) \
            .annotate(
                day_year=ExtractYear('order__created_at'),
                day_month=ExtractMonth('order__created_at')) \
            .values('day_year', 'day_month').annotate(
            total=Sum(F("price") * F('quantity'), output_field=models.FloatField())) \
            .values('day_year', 'day_month', 'total').order_by('day_year', 'day_month')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "2021-01-06", "total": 50.0}, {"day_year": "2021-01-09", "total": 10.0},
                    {"day_year": "2021-01-12", "total": 90.0}, {"day_year": "2021-01-13", "total": 70.0},
                    {"day_year": "2021-01-15", "total": 80.0}, {"day_year": "2021-01-22", "total": 22.0},
                    {"day_year": "2021-02-17", "total": 25.0}]

            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(months=i)
                data[count]['day_year'] = day.year
                data[count]['day_month'] = day.month
                count += 1
            return data

        return list(items)


class ShopOrderData(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'month':
            data = self.get_month_data(request, shop)
        if request.GET.get('type') == 'by_week':
            data = self.get_data_by_week(request, shop)
        elif request.GET.get('type') == 'by_month':
            data = self.get_data_by_month(request, shop)
        else:
            data = self.get_data_by_day(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_month_data(self, request, shop):
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
        if settings.ENABLE_DUMMY_DATA:
            return {
                'this_month': 20,
                'last_month': 9
            }
        return {
            'this_month': total_orders_this_month,
            'last_month': total_orders_last_month
        }

    def get_data_by_day(self, request, shop):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user) \
            .annotate(day=Trunc('order__created_at', 'day', output_field=models.DateField())) \
            .values('day').annotate(total=Count('order', distinct=True)) \
            .values('day', 'total').order_by('day')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day": "", "total": 1}, {"day": "", "total": 1}, {"day": "", "total": 1}, {"day": "", "total": 1},
                    {"day": "", "total": 2}, {"day": "", "total": 9}, {"day": "", "total": 1}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                data[count]['day'] = format("Y-m-d", today - relativedelta(days=i))
                count += 1
            return data

        return list(items)

    def get_data_by_week(self, request, shop):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user) \
            .annotate(
                day_year=ExtractYear('order__created_at'),
                day_week=ExtractWeek('order__created_at')) \
            .values('day_year', 'day_week').annotate(total=Count('order', distinct=True)) \
            .values('day_year', 'day_week', 'total').order_by('day_year', 'day_week')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "", "total": 1}, {"day_year": "", "total": 1},
                    {"day_year": "", "total": 1}, {"day_year": "", "total": 1},
                    {"day_year": "", "total": 2}, {"day_year": "", "total": 9},
                    {"day_year": "", "total": 1}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(weeks=i)
                data[count]['day_year'] = day.year
                data[count]['day_week'] = day.isocalendar()[1]
                count += 1

            return data

        return list(items)

    def get_data_by_month(self, request, shop):
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        items = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user) \
            .annotate(
                day_year=ExtractYear('order__created_at'),
                day_month=ExtractMonth('order__created_at')) \
            .values('day_year', 'day_month').annotate(total=Count('order', distinct=True)) \
            .values('day_year', 'day_month', 'total').order_by('day_year', 'day_month')

        if settings.ENABLE_DUMMY_DATA:
            data = [{"day_year": "", "total": 1}, {"day_year": "", "total": 1},
                    {"day_year": "", "total": 1}, {"day_year": "", "total": 1},
                    {"day_year": "", "total": 2}, {"day_year": "", "total": 9},
                    {"day_year": "", "total": 1}]
            today = datetime.date.today()
            count = 0
            for i in range(len(data), 0, -1):
                day = today - relativedelta(months=i)
                data[count]['day_year'] = day.year
                data[count]['day_month'] = day.month
                count += 1
            return data

        return list(items)


class ShopPopularProductsData(ListAPIView):
    serializer_class = ProductModelSimpleSerializer

    def get_queryset(self):
        shop = self.request.user.get_shop()
        type = self.request.GET.get('type')

        today = datetime.date.today()
        if type == 'this_week':
            day = today - relativedelta(weekday=today.weekday())
        elif type == 'this_month':
            day = datetime.date(today.year, today.month, 1)
        else:
            day = today

        product_ids = ProductView.objects.filter(product__shop=shop) \
           .filter(viewed_date__gte=day) \
           .values('product').annotate(total=Sum('count')) \
           .order_by('-total').values_list('product', flat=True)[:10]

        query_views = Subquery(
            ProductView.objects.filter(product=OuterRef('pk')) \
                .filter(viewed_date__gte=day) \
                .values('product').annotate(views_total=Sum('count')).values('views_total'))

        return Product.objects.filter(id__in=product_ids) \
            .annotate(views_count=query_views).order_by('-views_count')


class SalePieChartData(APIView):

    def get(self, request, *args, **kwargs):
        from dateutil.parser import parse
        shop = self.request.user.get_shop()
        try:
            filter_date = parse(request.GET.get('month'), yearfirst=True)
        except:
            filter_date = datetime.date.today()

        order_ids = OrderItem.objects.filter(product__shop=shop,
                                             created_at__year=filter_date.year,
                                             created_at__month=filter_date.month) \
            .values('order_id').distinct().values_list('order_id', flat=True)
        data = Order.objects.filter(id__in=order_ids).values('source') \
            .annotate(count=Count('source')) \
            .values('source', 'count')

        total = order_ids.count()
        results = []
        source_map = dict(Order.SOURCE_CHOICES)
        labels = []
        values = []
        titles = []
        for obj in data:
            value = round(obj['count'] / total * 100, 0)
            label = source_map.get(obj['source'], obj['source'])
            title = '{}% {}'.format(value, label)
            labels.append(label)
            values.append(value)
            titles.append(title)

        data = {
            'labels': labels,
            'data': values,
            'titles': titles
        }

        if settings.ENABLE_DUMMY_DATA:
            today = datetime.date.today()
            if filter_date.month == today.month and filter_date.year == today.year:
                data = {
                    'labels': ["Google Shopping", "Native Search"],
                    'titles': ["70% Google Shopping", "30% Native Search"],
                    'data': [70, 30]
                }
        return Response(data=data, status=status.HTTP_200_OK)


class OtherDataReport(APIView):

    def get(self, request, *args, **kwargs):
        this_month = datetime.date.today()

        shop = self.request.user.get_shop()
        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        avg_order_amount = OrderItem.objects.filter(product__shop=shop,
                                                    order__status__in=statuses,
                                                    created_at__year=this_month.year,
                                                    created_at__month=this_month.month
                                                    ).values('order') \
           .annotate(total=Sum(F("price") * F('quantity'), output_field=models.FloatField())) \
           .aggregate(avg_amount=Avg('total'))['avg_amount'] or 0

        avg_product_per_order = OrderItem.objects.filter(product__shop=shop,
                                                         order__status__in=statuses,
                                                         created_at__year=this_month.year,
                                                         created_at__month=this_month.month).values('order') \
            .annotate(total=Count("product")) \
            .aggregate(avg_num_product=Avg('total'))['avg_num_product'] or 0
        data = {
            'avg_order_amount': round(avg_order_amount, 0),
            'avg_product_per_order': round(avg_product_per_order, 1)
        }
        if settings.ENABLE_DUMMY_DATA:
            data = {
                'avg_order_amount': 32.50,
                'avg_product_per_order': 2
            }
        return Response(data=data, status=status.HTTP_200_OK)


class StoreVisitView(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'today':
            data = self.get_data_by_day(request, shop)
        elif request.GET.get('type') == 'this_week':
            data = self.get_data_by_week(request, shop)
        else:
            data = self.get_data_by_month(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_data_by_day(self, request, shop):
        today = datetime.date.today()

        count = StorefrontView.objects.filter(shop=shop,
                                              viewed_date=today) \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0

        return {"count": count}

    def get_data_by_week(self, request, shop):
        today = datetime.date.today()
        this_week = today - datetime.timedelta(days=today.weekday())

        count = StorefrontView.objects.filter(shop=shop,
                                              viewed_date=this_week) \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0

        return {"count": count}

    def get_data_by_month(self, request, shop):
        today = datetime.date.today()

        count = StorefrontView.objects.filter(shop=shop,
                                              viewed_date__year=today.year,
                                              viewed_date__month=today.month,) \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0

        return {"count": count}


class ProductViewCount(APIView):

    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'today':
            data = self.get_data_by_day(request, shop)
        elif request.GET.get('type') == 'this_week':
            data = self.get_data_by_week(request, shop)
        else:
            data = self.get_data_by_month(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_data_by_day(self, request, shop):
        today = datetime.date.today()

        count = ProductView.objects.filter(product__shop=shop,
                                           viewed_date=today) \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0

        return {"count": count}

    def get_data_by_week(self, request, shop):
        today = datetime.date.today()
        this_week = today - datetime.timedelta(days=today.weekday())

        count = ProductView.objects.filter(product__shop=shop,
                                           viewed_date__gte=this_week) \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0

        return {"count": count}

    def get_data_by_month(self, request, shop):
        today = datetime.date.today()

        count = ProductView.objects.filter(product__shop=shop,
                                           viewed_date__year__gte=today.year,
                                           viewed_date__month__gte=today.month,) \
           .aggregate(this_month_count=Sum('count'))['this_month_count'] or 0

        return {"count": count}


class OrderCountView(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'today':
            data = self.get_data_by_day(request, shop)
        elif request.GET.get('type') == 'this_week':
            data = self.get_data_by_week(request, shop)
        else:
            data = self.get_data_by_month(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_data_by_day(self, request, shop):
        today = datetime.date.today()

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        count = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__day=today.day,
                                         created_at__month=today.month,
                                         created_at__year=today.year).values("order").distinct().count()

        return {"count": count}

    def get_data_by_week(self, request, shop):
        today = datetime.date.today()
        this_week = today - datetime.timedelta(days=today.weekday())

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        count = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__gte=this_week).values("order").distinct().count()

        return {"count": count}

    def get_data_by_month(self, request, shop):
        today = datetime.date.today()

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        count = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__month=today.month,
                                         created_at__year=today.year).values("order").distinct().count()

        return {"count": count}


class RevenueTotalView(APIView):
    def get(self, request, *args, **kwargs):
        shop = request.user.get_shop()

        if request.GET.get('type') == 'today':
            data = self.get_data_by_day(request, shop)
        elif request.GET.get('type') == 'this_week':
            data = self.get_data_by_week(request, shop)
        else:
            data = self.get_data_by_month(request, shop)

        return Response(data=data, status=status.HTTP_200_OK)

    def get_data_by_day(self, request, shop):
        today = datetime.date.today()

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        total = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__day=today.day,
                                         created_at__month=today.month,
                                         created_at__year=today.year) \
            .aggregate(
                total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0

        return {"total": total}

    def get_data_by_week(self, request, shop):
        today = datetime.date.today()
        this_week = today - datetime.timedelta(days=today.weekday())

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        total = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__gte=this_week) \
            .aggregate(
                total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0

        return {"total": total}

    def get_data_by_month(self, request, shop):
        today = datetime.date.today()

        statuses = [
            Order.Status.SHIPPED,
            Order.Status.AWAITING_SHIPMENT,
            Order.Status.ON_HOLD,
        ]
        total = OrderItem.objects.filter(order__status__in=statuses,
                                         product__shop__owner=request.user,
                                         created_at__month=today.month,
                                         created_at__year=today.year) \
            .aggregate(
                total=Sum(F("price") * F('quantity'), output_field=models.FloatField()))['total'] or 0

        return {"total": total}


class TopProductsAddToCart(ListAPIView):
    serializer_class = ProductModelSimpleSerializer

    def get_queryset(self):
        shop = self.request.user.get_shop()
        type = self.request.GET.get('type')

        today = datetime.date.today()
        if type == 'this_week':
            day = today - relativedelta(weekday=today.weekday())
        elif type == 'this_month':
            day = datetime.date(today.year, today.month, 1)
        else:
            day = today

        product_ids = ProductAddedToCart.objects.filter(
            product__shop=shop, added_date__gte=day).values_list('product', flat=True)

        query = Subquery(
            ProductAddedToCart.objects.filter(product=OuterRef('pk')) \
                .filter(added_date__gte=day) \
                .values('product').annotate(total=Sum('count')).values('total'))
        return Product.objects.filter(id__in=product_ids) \
            .annotate(product_add_to_cart_count=query).order_by('-product_add_to_cart_count')
