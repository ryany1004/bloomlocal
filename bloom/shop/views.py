import django
from django.conf import settings
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import baseconv, timezone
from django.views.generic.base import View
from google.cloud.storage import Bucket, Blob

from bloom.shop.models import Shop, Product
from bloom.users.models import UserRole


class HomePage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_type == UserRole.BUSINESS:
            return render(request, 'pages/business_dashboard.html', {"page": 'dashboard'})

        return render(request, 'pages/home.html')


class InventoryPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/business/products.html', {"page": 'inventory'})


class MyOrderPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/business/my_orders.html', {"page": 'my_order'})


class ProductUpload(View):
    def get(self, request, *args, **kwargs):
        shop = request.user.shop_set.first()
        if not shop:
            shop = Shop(owner=request.user, name=request.user)
            shop.save()

        return render(request, 'pages/business/product_add.html', context={'shop': shop, 'page':'upload'})


class ProductUpdate(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, uuid=kwargs['uuid'])
        shop = product.shop
        context = {
            'shop': shop,
            'page': 'update',
            'product': product,
        }
        return render(request, 'pages/business/product_update.html', context=context)
