import django
from django.conf import settings
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from google.cloud.storage import Bucket, Blob
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bloom.shop.api.serializers import AttributeValueSerializer, CategorySerializer, ProductSerializer, \
    ProductModelSerializer
from bloom.shop.models import AttributeValue, Category, Product
import datetime
import json
import random
import string
from datetime import time
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

    def get_queryset(self):
        return AttributeValue.objects.filter(attribute__attribute_code=self.kwargs['code'])


class CategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent=None)


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


class ShopProductListAPI(ListAPIView):
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        return Product.objects.select_related('shop').prefetch_related('productimage_set', 'productvariant_set') \
            .filter(shop=self.request.user.get_shop())
