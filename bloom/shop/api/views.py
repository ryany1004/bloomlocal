import django
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from google.cloud.storage import Bucket, Blob
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, \
    RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.order.models import OrderItem, Order
from bloom.shop.api.pagination import StandardResultsSetPagination
from bloom.shop.api.serializers import AttributeValueSerializer, CategorySerializer, ProductSerializer, \
    ProductModelSerializer, ShopSerializer, ShopCategorySerializer
from bloom.shop.models import AttributeValue, Category, Product, Shop, ShopCategory
import datetime
import random
import string
from bloom.utils.bucket_registry import _bucket_registry

URLSAFE_CHARACTERS = string.ascii_letters + string.digits + "-._~"
REQUIRED_PARAMS = ['filename', 'content_type']
signer = django.core.signing.Signer()


class BaseAPIView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(BaseAPIView, self).dispatch(*args, **kwargs)


class AttributeValueAPIView(ListAPIView):
    serializer_class = AttributeValueSerializer
    permission_classes = []

    def get_queryset(self):
        attributes = cache.get('attribute_{}'.format(self.kwargs['code']))
        if not attributes:
            attributes = AttributeValue.objects.filter(attribute__attribute_code=self.kwargs['code'])
            cache.set('attribute_{}'.format(self.kwargs['code']), attributes)
        return attributes


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
            product_ids = OrderItem.objects.filter(order__status=Order.Status.SUCCEED, product__shop=shop) \
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
            product_ids = OrderItem.objects.filter(order__status=Order.Status.SUCCEED,
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
            shop_ids = OrderItem.objects.filter(order__status=Order.Status.SUCCEED) \
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
    serializer_class = ProductModelSerializer
    permission_classes = []

    def get_queryset(self):
        query = self.request.GET.get("query")
        return Product.objects.select_related('shop') \
            .prefetch_related('productimage_set', 'productvariant_set', 'categories') \
            .filter(Q(title__icontains=query) | Q(description__icontains=query), status=0, archived=False)[:50]


class ShopSearch(ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = []

    def get_queryset(self):
        query = self.request.GET.get("query")
        return Shop.objects.select_related('owner').prefetch_related('categories') \
            .filter(name__icontains=query)[:50]
