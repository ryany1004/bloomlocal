import json
import os
import urllib.request

import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos.point import Point
from django.contrib.gis.measure import D
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.core.files.base import File
from django.db import transaction
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from google.cloud.storage import Bucket, Blob
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, \
    RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.order.models import OrderItem, Order
from bloom.users.models import ShopifyShop, WordpressShop
from bloom.utils.pagination import StandardResultsSetPagination
from bloom.shop.api.serializers import CategorySerializer, ProductSerializer, \
    ProductModelSerializer, ShopSerializer, ShopCategorySerializer, ProductSearchSerializer, ShopSearchSerializer
from bloom.shop.models import Category, Product, Shop, ShopCategory, Attribute, ProductImage, ProductVariant, \
    ImageStorage
import datetime
import random
import string
from bloom.utils.bucket_registry import _bucket_registry
from bloom.utils.shopping import save_product_data

URLSAFE_CHARACTERS = string.ascii_letters + string.digits + "-._~"
REQUIRED_PARAMS = ['filename', 'content_type']
signer = django.core.signing.Signer()
User = get_user_model()


class BaseAPIView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(BaseAPIView, self).dispatch(*args, **kwargs)


class AttributeValueAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        attribute = cache.get('attribute_{}'.format(self.kwargs['code']))
        if not attribute:
            attribute = Attribute.objects.get(attribute_code=self.kwargs['code'])
            cache.set('attribute_{}'.format(self.kwargs['code']), attribute)

        return Response(data=attribute.values, status=status.HTTP_200_OK)


class CategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = []

    def get_queryset(self):
        categories = cache.get('product_categories')
        if not categories:
            categories = Category.objects.filter(parent=None)
            cache.set('product_categories', categories)
        return categories


class UploadURLAPI(BaseAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        for p in REQUIRED_PARAMS:

            if not request.data.get(p):
                return Response(f"'{p}' is a required parameter.", status=status.HTTP_400_BAD_REQUEST)

        bucketname, path_prefix = settings.GS_BUCKET_NAME, 'product/'
        bucket: Bucket = _bucket_registry.get('gs://' + bucketname)
        if not bucket:
            return Response(f"Unknown bucket identifier 'gs://{bucketname}'.", status=status.HTTP_400_BAD_REQUEST)

        filename: str = request.data['filename']
        content_type: str = request.data['content_type']
        if len(filename) > 200:
            filename = filename[len(filename) - 200:]

        timestring: str = "{0:%Y-%m-%d_%H-%M-%S/}".format(timezone.now())
        randomstring: str = "".join(random.choices(URLSAFE_CHARACTERS, k=24))
        path_prefix = request.data['prefix'] if request.data.get('prefix') else path_prefix
        path: str = f"{path_prefix}{timestring}{randomstring}/{filename}"
        blob: Blob = bucket.blob(f"media/{path}")

        return Response({
            'url': blob.generate_signed_url(
                expiration=timezone.now() + datetime.timedelta(seconds=1000),
                method='PUT',
                content_type=content_type,
            ),
            'path': path,
            'public_url': settings.MEDIA_URL + path
        }, status=status.HTTP_200_OK)


class UploadProductAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = ProductSerializer(data=request.data)
        if data.is_valid():
            data.save()
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class UpdateAttributeProductAPI(APIView):
    def patch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, uuid=kwargs['uuid'], shop__owner=request.user)
        data = ProductSerializer(data=request.data, partial=True, instance=product)
        if data.is_valid():
            data.save()
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=ProductModelSerializer(instance=product).data)


class ShopProductListAPI(ListAPIView):
    serializer_class = ProductModelSerializer
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        shop = self.request.user.get_shop()
        if self.request.GET.get('view') == 'recent_added':
            return Product.objects.select_related('shop') \
                .prefetch_related('productimage_set', 'productvariant_set', 'categories') \
                .filter(shop=shop, archived=False).order_by('-created_at')[:20]

        elif self.request.GET.get('view') == 'best_selling':
            statuses = [
                Order.Status.SHIPPED,
                Order.Status.AWAITING_SHIPMENT,
                Order.Status.ON_HOLD
            ]
            product_ids = OrderItem.objects.filter(order__status__in=statuses, product__shop=shop) \
                .values('product_id').annotate(total=Count('product_id')) \
                .order_by('-total').values_list('product_id', flat=True)[:50]
            return Product.objects.select_related('shop') \
                .prefetch_related('productimage_set', 'productvariant_set','categories') \
                .filter(id__in=product_ids, archived=False)

        return Product.objects.select_related('shop') \
            .prefetch_related('productimage_set', 'productvariant_set','categories') \
            .filter(shop=shop, archived=False)


class PublishShopProductList(ShopProductListAPI):
    permission_classes = []

    def get_queryset(self):
        if self.request.GET.get('view') == 'recent_added':
            return Product.objects.select_related('shop') \
                       .prefetch_related('productimage_set', 'productvariant_set', 'categories') \
                       .filter(shop_id=self.kwargs['shop_id'], archived=False, status=0).order_by('-created_at')[:20]

        elif self.request.GET.get('view') == 'best_selling':
            statuses = [
                Order.Status.SHIPPED,
                Order.Status.AWAITING_SHIPMENT,
                Order.Status.ON_HOLD
            ]
            product_ids = OrderItem.objects.filter(order__status__in=statuses,
                                                   product__shop_id=self.kwargs['shop_id']) \
                              .values('product_id').annotate(total=Count('product_id')) \
                              .order_by('-total').values_list('product_id', flat=True)[:50]
            return Product.objects.select_related('shop') \
                .prefetch_related('productimage_set', 'productvariant_set', 'categories') \
                .filter(id__in=product_ids, archived=False)

        return Product.objects.select_related('shop') \
            .prefetch_related('productimage_set', 'productvariant_set', 'categories') \
            .filter(shop=self.kwargs['shop_id'], status=0, archived=False)


class ProductDetails(RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = ProductModelSerializer

    def get_object(self):
        return get_object_or_404(Product, uuid=self.kwargs['uuid'])


class ShopListAPI(ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = []
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('view') == 'recent_added':
            return Shop.objects.select_related('owner') \
                       .prefetch_related('categories').order_by('-created_at')[:20]
        elif self.request.GET.get('view') == 'best_selling':
            statuses = [
                Order.Status.SHIPPED,
                Order.Status.AWAITING_SHIPMENT,
                Order.Status.ON_HOLD
            ]
            shop_ids = OrderItem.objects.filter(order__status__in=statuses) \
                              .values('product__shop').annotate(total=Count('product__shop')) \
                              .order_by('-total').values_list('product__shop', flat=True)[:50]
            return Shop.objects.select_related('owner') \
                       .prefetch_related('categories').filter(id__in=shop_ids)
        return Shop.objects.select_related('owner') \
            .prefetch_related('categories')


class ShopCategoryAPIView(ListAPIView):
    serializer_class = ShopCategorySerializer
    permission_classes = []

    def get_queryset(self):
        categories = cache.get('shop_categories')
        if not categories:
            categories = ShopCategory.objects.filter(parent=None)
            cache.set('shop_categories', categories)
        return categories


class ProductSearch(ListAPIView):
    serializer_class = ProductSearchSerializer
    permission_classes = []

    def get_queryset(self):
        request = self.request
        query = self.request.GET.get("query")
        kwargs = {}
        if request.user.is_authenticated and request.user.role_type == '1':
            kwargs['shop__owner'] = request.user

        queryset = Product.objects.select_related('shop') \
            .prefetch_related('productimage_set', 'productvariant_set', 'categories') \
            .filter(Q(title__icontains=query) | Q(description__icontains=query),
                    status=0, archived=False, **kwargs)

        if 'lat' in request.GET and 'long' in request.GET:
            point = Point((float(request.GET['lat']), float(request.GET['long'])))
            queryset = queryset.filter(shop__location__distance_lte=(point, D(km=settings.SEARCH_DISTANCE_IN_KM)))

        return queryset[:50]


class ShopSearch(ListAPIView):
    serializer_class = ShopSearchSerializer
    permission_classes = []

    def get_queryset(self):
        request = self.request
        query = request.GET.get("query")
        queryset = Shop.objects.select_related('owner').prefetch_related('categories') \
                       .filter(name__icontains=query)
        if 'lat' in request.GET and 'long' in request.GET:
            point = Point((float(request.GET['lat']), float(request.GET['long'])))
            queryset = queryset.filter(location__distance_lte=(point, D(km=settings.SEARCH_DISTANCE_IN_KM)))
        return queryset[:50]


class ShopifyImportProduct(APIView):

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        data = request.data
        shop = request.user.get_shop()
        p = Product.objects.filter(shopify_product_id=data['id'], shop=shop).first()
        if not p:
            p = Product()
            p.shopify_product_id = data['id']
            p.shop = shop

        save_product_data(p, data)

        return Response(status=status.HTTP_200_OK)


class WordpressImportProduct(APIView):

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        data = request.data
        shop = request.user.get_shop()
        p = Product.objects.filter(wp_product_id=data['id'], shop=shop).first()
        if not p:
            p = Product()
            p.wp_product_id = data['id']
            p.shop = shop

        save_product_data(p, data)

        return Response(status=status.HTTP_200_OK)


class FileImportProductStorefront(APIView):
    permission_classes = []

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        data = request.data
        p = Product()
        if request.user.is_authenticated:
            p.shop = request.user.get_shop()
        else:
            user_id = request.session.get('register_user')
            user = get_object_or_404(User, pk=user_id)
            p.shop = user.get_shop()

        save_product_data(p, data)
        return Response(status=status.HTTP_200_OK)


class SpreadsheetPermissionURL(APIView):
    def post(self, request, *args, **kwargs):
        file_url = request.data['file_url']
        import re
        search = re.compile(r'/d/(\w+)/')
        sheet_id = search.search(file_url).group(1)
        request.session['sheet_id'] = sheet_id

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        redirect_uri = request.build_absolute_uri(reverse('shop:spreadsheet-callback'))
        credentials_path = str(settings.ROOT_DIR / settings.SPREADSHEET_CREDENTIALS)
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES, redirect_uri=redirect_uri)
        auth_url, _ = flow.authorization_url(prompt='consent')
        return Response(data={'auth_url': auth_url}, status=status.HTTP_200_OK)


class ShopUpdateView(UpdateAPIView):
    serializer_class = ShopSerializer
    permission_classes = []

    def get_object(self):
        user_id = self.request.session.get('register_user')
        user = get_object_or_404(User, pk=user_id)
        shop = user.get_shop()
        return shop


class ShopifyURLUpdateView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        shop_url = request.data['shop_url']
        user_id = request.session.get('register_user')
        user = get_object_or_404(User, pk=user_id)
        shop = ShopifyShop.objects.get_or_create(user=user)[0]
        shop.shop_url = shop_url
        shop.save()

        return Response(status=status.HTTP_200_OK)


class WooURLUpdateView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        shop_url = request.data['shop_url']
        user_id = request.session.get('register_user')
        user = get_object_or_404(User, pk=user_id)
        shop = WordpressShop.objects.get_or_create(user=user)[0]
        shop.shop_url = shop_url
        shop.save()

        return Response(status=status.HTTP_200_OK)
