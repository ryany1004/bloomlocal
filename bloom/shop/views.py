import django
from django.conf import settings
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.utils import baseconv, timezone
from django.views.generic.base import View
from google.cloud.storage import Bucket, Blob

from bloom.shop.models import Shop
from bloom.users.models import UserRole


class HomePage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_type == UserRole.BUSINESS:
            return render(request, 'pages/business_dashboard.html')

        return render(request, 'pages/home.html')


class ProductUpload(View):
    def get(self, request, *args, **kwargs):
        shop = request.user.shop_set.first()
        if not shop:
            shop = Shop(owner=request.user, name=request.user)
            shop.save()

        return render(request, 'pages/business/product_add.html', context={'shop': shop, 'page':'upload'})

